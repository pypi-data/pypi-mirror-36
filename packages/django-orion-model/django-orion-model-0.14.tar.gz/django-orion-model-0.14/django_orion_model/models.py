from datetime import timedelta

from django.conf import settings
from django.contrib.postgres.fields import JSONField, ArrayField
from django.db import models

# Create your models here.
from django.utils.timezone import now
from pyfiware import OrionConnector
from pyfiware.oauth import OAuthManager
from logging import getLogger


logger = getLogger(__name__)


def _expire_time():
    return now() + timedelta(seconds=settings.ORION_EXPIRATION)


def _orion_get(self, item):
    _get = super().__getattribute__
    if item in _get('_orion_fields'):
        self.refresh_orion()
    return _get(item)


def _orion_set(self, key, value):
    if key in self._orion_fields:
        self.updated.append(key)
        self.save_to_orion()
    super().__setattr__(key, value)


class ContextBroker(models.Model):
    """ Identifies  a Orion context context_broker by a human friendly  name and stores its url.
        """
    name = models.CharField(unique=True, max_length=50)
    url = models.URLField()
    oauth_enable = models.BooleanField(default=False)
    oauth_url = models.URLField(blank=True)
    oauth_user = models.CharField(blank=True, max_length=50)
    oauth_password = models.CharField(blank=True, max_length=50)
    oauth_client_id = models.CharField(blank=True, max_length=50)
    oauth_client_secret = models.CharField(blank=True, max_length=50)
    oauth_access_token = models.CharField(blank=True, max_length=50)
    oauth_refresh_token = models.CharField(blank=True, max_length=50)

    @property
    def oauth_manager(self):
        return self.oauth_enable and OAuthManager(
                oauth_server_url=self.oauth_url,
                client_id=self.oauth_client_id,
                client_secret=self.oauth_client_secret,
                user=self.oauth_user,
                password=self.oauth_password,
                token=self.oauth_access_token,
                refresh_token=self.oauth_refresh_token
            )

    def __str__(self):
        return "{0}({1})".format(self.name, self.url)


class Service(models.Model):
    context_broker = models.ForeignKey(ContextBroker, on_delete=models.CASCADE, )
    name = models.CharField(unique=True, max_length=50)
    path = models.CharField(max_length=65000)

    def __str__(self):
        return "{0}({1})".format(self.name, self.path)


class ServicePath(models.Model):
    """ Identifies a Orion service path by a human friendly name and stores its path form.
    """
    service = models.ForeignKey(Service, on_delete=models.CASCADE,)
    name = models.CharField(unique=True, max_length=50)
    path = models.CharField(max_length=65000)

    @property
    def connector(self):
        return OrionConnector(
            host=self.service.context_broker.url,
            service=self.service.path,
            service_path=self.path,
            oauth_connector=self.service.context_broker.oauth_manager
            )

    def __str__(self):
        return "{0}({1})".format(self.name, self.path)

    def search(self, entity_type=None, id_pattern=None, query=None):
        """Find suitable entities from Orion"""
        response = self.connector.search(entity_type=entity_type, id_pattern=id_pattern, query=query)
        return [entity for entity in response]

    def remove_form_orion(self, orion_id, entity_type):
        """ Ask Orion to remove a entity"""
        self.connector.delete(entity_id=orion_id, entity_type=entity_type)


class OrionEntity(models.Model):
    """ Stores a local Entity. Its includes the connection to Orion context broker and the necesary information to


    """
    ORION_TYPE = "Entity"
    ORION_SUB_TYPE = None

    # Created and awaiting to be pushed to Orion
    STATUS_CREATING = "CREATING"
    # Created and awaiting to be populated from Orion
    STATUS_CREATED = "CREATED"
    # The mention is currently writing from orion
    STATUS_PENDING_WRITING = "WRITING"
    # The mention is currently reading from orion
    STATUS_PENDING_READING = "READING"
    # The Entity does not need to write or read from Orion
    STATUS_OK = "OK"
    # The mention awaits for repeat a writing
    STATUS_AWAIT_REWRITING = "REWRITING"
    # The mention awaits for repeat a reading
    STATUS_AWAIT_REFRESH = "REFRESH"
    # The entity is not connected to Orion
    STATUS_OFFLINE = "OFFLINE"
    # The mention does not have a reflect in Orion
    STATUS_MISSING = "MISSING"

    STATUS_OPTIONS = [
        (STATUS_CREATING, "Creating"),
        (STATUS_CREATED, "Created"),
        (STATUS_PENDING_WRITING, "Pending writing"),
        (STATUS_PENDING_READING, "Pending reading"),
        (STATUS_OK, "Ok"),
        (STATUS_AWAIT_REFRESH, "Await refresh"),
        (STATUS_AWAIT_REWRITING, "Await rewrite"),
        (STATUS_OFFLINE, "Offline"),
        (STATUS_MISSING, "Missing"),
    ]

    CREATION_ACTIONS = [
        (STATUS_CREATED, "Existing"),
        (STATUS_CREATING, "New"),
        (STATUS_OFFLINE, "Offline"),
    ]
    orion_service_path = models.ForeignKey(ServicePath, models.CASCADE)

    orion_id = models.CharField(unique=True, max_length=1011)
    orion_type = models.CharField(max_length=1011)
    orion_data = JSONField(blank=True, default=dict)

    orion_updated = ArrayField(models.CharField(max_length=100), blank=True, default=list)
    orion_expiration = models.DateTimeField(default=_expire_time, blank=True)
    orion_status = models.CharField(blank=True, default="created", max_length=50, choices=STATUS_OPTIONS)
    orion_error = models.TextField(blank=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Check without triggering Orion sync if entity have a type, if no  load with class default
        self.orion_type = getattr(self, "orion_type", None) or getattr(self, "ORION_TYPE", None)
        if self.orion_type is None:
            raise Exception("Set entity type as orion_type parameter or orion_type_default class attribute")

        self._orion_fields = set(f.attname for f in self._meta.fields if issubclass(type(f), OrionField))
        self.__getattribute__ = _orion_get
        self.__setattr__ = _orion_set

    def class_name(self):
        return self.__class__.__name__

    @property
    def history_cache(self):
        return self._history_cache

    @history_cache.setter
    def history_cache(self, value):
        self._history_cache = value

    def history(self, time_slice):
        if type(time_slice) is list:
            return [[key, self.history_cache.get(key, None)] for key in time_slice]
        return self.history_cache.fromkeys(time_slice)

    @classmethod
    def from_db(cls, db, field_names, values):
        """Override model save methods """
        orion_object = super().from_db(db, field_names, values)
        orion_object.update_from_orion()
        return orion_object

    def save(self, *args, **kwargs):
        """Override model save methods """
        self.save_to_orion()
        super().save(*args, **kwargs)

    # Orion Connectivity
    def refresh_orion(self):
        reload = self.orion_expiration > now()
        if self.orion_status == self.STATUS_CREATED:
            logger.warning("Lecture of %s while unset", self.orion_id)
            reload = True
        elif self.orion_status == self.STATUS_PENDING_WRITING:
            logger.warning("Lecture of %s while transition status %s", self.orion_id, self.orion_status)
        elif self.orion_status == self.STATUS_PENDING_READING:
            logger.warning("Lecture of %s while transition status %s", self.orion_id, self.orion_status)
            reload = True
        elif self.orion_status == self.STATUS_AWAIT_REFRESH:
            reload = True
        if reload:
            self.update_from_orion()
        for key in self.orion_data:
            try:
                super().__setattr__(key, self.orion_data[key])
            except KeyError:
                pass

    def save_to_orion(self):
        """ Saves the object to Orion context context_broker.

        If an error occurs object is marked as STATUS_AWAIT_REWRITING and keeps update flags.
        If everything goes correctly update flags are resets and a reading is launched.

        :return: Nothing
        """
        if self.orion_status == self.STATUS_OFFLINE:
            return

        if self.orion_status == self.STATUS_CREATING:
            attributes = self.orion_data
            for field in self._orion_fields:
                attributes[field] = super().__getattribute__(field)
            try:
                self.orion_updated = []
                self.orion_service_path.connector.create(element_id=self.orion_id, element_type=self.orion_type, **attributes)
                self.update_from_orion()

            except Exception as ex:
                self.orion_error = "Error creating: {0}".format(ex)
                self.orion_status = self.STATUS_AWAIT_REWRITING
            return

        self.orion_status = self.STATUS_PENDING_WRITING
        try:
            if self.orion_updated:
                update_json = {}
                for field in self.orion_updated:
                    update_json[field] = self.orion_data[field]
                self.orion_service_path.connector.patch(element_id=self.orion_id, **update_json)
                self.orion_updated = []
            self.update_from_orion()
        except Exception as ex:
            self.orion_error = str(ex)
            self.orion_status = self.STATUS_AWAIT_REWRITING

    def update_from_orion(self):
        """ The object data is updated from the Orion context context_broker.

        If an error occurs object is marked as STATUS_AWAIT_REFRESH and awaits keeps old data
        If everything goes correctly data is stored, expiration mark is set and object is marked as STATUS_OK.

        :return: Nothing
        """
        if self.orion_status == self.STATUS_OFFLINE:
            return

        self.orion_status = self.STATUS_PENDING_READING
        try:
            response = self.orion_service_path.connector.get(entity_id=self.orion_id, silent=True)
            if response:
                self.orion_data = response
                self.orion_expiration = _expire_time()
                self.orion_type = self.orion_data.get("type")
                for field in self._orion_fields:
                    if field is OrionField:
                        field.update_from_json()
                self.orion_status = self.STATUS_OK
            else:
                self.orion_status = self.STATUS_MISSING
        except Exception as ex:
            self.orion_error = str(ex)
            self.orion_expiration = now()
            self.orion_status = self.STATUS_AWAIT_REFRESH


class OrionField:
    orion_field = True


class OrionCharField(models.CharField, OrionField):
    pass


class OrionTextField(models.TextField, OrionField):
    pass


class OrionFloatField(models.FloatField, OrionField):
    pass


class OrionDateTimeField(models.DateTimeField, OrionField):
    pass
