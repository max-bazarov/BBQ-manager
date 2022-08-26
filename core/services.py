import logging
from typing import Optional

import funcy
from django import forms
from django.core.exceptions import FieldDoesNotExist, ValidationError
from django.db.models import Model
from rest_framework.serializers import Serializer
from service_objects.services import Service

log = logging.getLogger(__name__)


class BaseService:
    '''
    Base Service provides funcionality for basic operations with model instances.

    Usage: use this class as a mixin for other services.
    '''

    model: type[Model]
    serializer_class: Optional[type[Serializer]]
    related_name: str
    archivable_relation: bool = True

    def __init__(self, instance: Optional[Model] = None,
                 data: dict = None,
                 **kwargs) -> None:
        self.instance = instance
        self._kwargs = kwargs
        self.partial = self._kwargs.get('partial', False)
        self.data = data
        print(self.model.__name__, hasattr(self.model, 'archive'))

    def has_related(self):
        if not self.related_name:
            return False
        return getattr(self.instance, self.related_name).exists()

    def is_all_related_archived(self):
        if not self.related_name:
            return True
        return not getattr(self.instance, self.related_name).filter(archived=False).exists()

    def _validate_data(self) -> dict:
        serializer = self.serializer_class(data=self.data, partial=self.partial)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data

    def _get_instance_data(self, omit_id: bool = True) -> dict:
        '''Is needed for validation that we do not save the same data twice.'''

        data = {}
        for field in self.instance._meta.fields:
            data[field.name] = getattr(self.instance, field.name)
        if not omit_id:
            return data
        return funcy.omit(data, ['id'])

    def archive(self):
        if not hasattr(self.instance, 'archived'):
            raise FieldDoesNotExist(f'{self.model.__name__} does not have field archived.')
        self.instance.archived = True
        self.instance.save()
        return self.instance

    def update(self) -> Model:
        for k, v in self._validate_data().items():
            setattr(self.instance, k, v)
        self.instance.save()
        return self.instance

    def create(self) -> Model:
        return self.model.objects.get_or_create(**self._validate_data())

    def destroy(self) -> int:
        print('destroy', self.instance, hasattr(self.model, 'archived'))
        if self.has_related():
            if self.archivable_relation and self.is_all_related_archived():
                self.archive()
                return self.instance.id
            raise ValidationError(
                f'Instance of model {self.model.__name__} cannot be deleted '
                'as it has unarchived related objects.'
            )
        self.model.objects.get(id=self.instance.id).delete()
        return self.instance.id


class ModelCreateService:

    def process(self):
        log.warning(
            f'Service {self.__class__.__name__} is depricated. '
            f'Do not use ModelCreateService as mixin.'
        )
        return self.model.objects.create(**self.cleaned_data)

    class Meta:
        abstract = True


class ModelDestroyService(Service):
    id = forms.IntegerField()

    def process(self):
        log.warning(
            f'Service {self.__class__.__name__} is depricated. '
            f'Do not use ModelDestroyService as mixin.'
        )
        self.model.objects.filter(**self.cleaned_data).delete()


class ArchiveService:
    instance: Model
    serializer_class: Optional[type[Serializer]]

    def __init__(self, instance: Model,
                 serializer_class: Optional[type[Serializer]] = None) -> None:

        self.instance = instance
        self.serializer_class = serializer_class

    def get_data(self, **kwargs):
        if not self.serializer_class:
            return kwargs

        serialzier = self.serializer_class(data=kwargs, partial=True)
        serialzier.is_valid(raise_exception=True)
        return serialzier.validated_data

    def _clean_data(self, **kwargs):
        kwargs = funcy.project(kwargs, [f.name for f in self.instance._meta.fields])
        data = {}
        for field in self.instance._meta.fields:
            data[field.name] = getattr(self.instance, field.name)
        data.update(kwargs)
        return funcy.omit(data, ['id', 'archived'])

    def update(self, **kwargs) -> Model:
        cleaned_data = self._clean_data(**kwargs)
        if len(cleaned_data) == 0:
            raise ValidationError('No data to update.')
        self.archive()
        new_instance = self.instance.__class__.objects.create(
            **self.get_data(**cleaned_data)
        )

        return new_instance

    def archive(self) -> int:
        if not hasattr(self.instance, 'archived'):
            raise FieldDoesNotExist(
                f'{self.instance.__class__.__name__} has no archived field'
            )
        self.instance.archived = True
        self.instance.save()
        return self.instance.pk
