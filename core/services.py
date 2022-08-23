import logging
from typing import Optional

import funcy
from django import forms
from django.core.exceptions import FieldDoesNotExist, ValidationError
from django.db.models import Model
from rest_framework.serializers import Serializer
from service_objects.services import Service

log = logging.getLogger(__name__)


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

    def __init__(self, instance: Model, serializer_class: Optional[type[Serializer]] = None) -> None:
        self.instance = instance
        self.serializer_class = serializer_class

    def get_data(self, **kwargs):
        if not self.serializer_class:
            return kwargs
        for k, v in kwargs.items():
            if isinstance(v, list):
                kwargs[k] = v.pop()
        serializer = self.serializer_class(data=kwargs, partial=True)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data

    def _clean_data(self, **kwargs):
        kwargs = funcy.project(kwargs, [f.name for f in self.instance._meta.fields])
        data = {}
        for field in self.instance._meta.fields:
            data[field.name] = getattr(self.instance, field.name)
        data.update(kwargs)
        print('clean data', data)
        return funcy.omit(data, ['id', 'archived'])

    def update(self, **kwargs) -> Model:
        print('update', kwargs)
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
