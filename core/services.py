import logging

import funcy
from django import forms
from django.core.exceptions import FieldDoesNotExist, ValidationError
from django.db.models import Model
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

    def __init__(self, instance: Model) -> None:
        self.instance = instance

    def update(self, **kwargs) -> Model:
        self.archive()
        kwargs = funcy.project(kwargs, [f.name for f in self.instance._meta.fields])
        if not kwargs:
            raise ValidationError('No data to update')
        data = {}
        for field in self.instance._meta.fields:
            data[field.name] = field.value_from_object(self.instance)
        data.update(kwargs)
        new_instance = self.instance.__class__.objects.create(**funcy.omit(data, ['id', 'archived']))
        return new_instance

    def archive(self) -> int:
        if not hasattr(self.instance, 'archived'):
            raise FieldDoesNotExist(
                f'{self.instance.__class__.__name__} has no archived field'
            )
        self.instance.archived = True
        self.instance.save()
        return self.instance.pk
