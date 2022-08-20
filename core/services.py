from django import forms
from django.core.exceptions import FieldDoesNotExist, ValidationError
from django.db.models import Model

import funcy

from service_objects.services import Service


class ModelCreateService:

    def process(self):
        return self.model.objects.create(**self.cleaned_data)

    class Meta:
        abstract = True


class ModelDestroyService(Service):
    id = forms.IntegerField()

    def process(self):
        self.model.objects.filter(**self.cleaned_data).delete()


class ArchiveService:

    def __init__(self, instance: Model) -> None:
        self.instance = instance

    def update(self, **kwargs) -> Model:
        self.archive()
        kwargs = funcy.project(kwargs, [f.name for f in self.instance._meta.fields])
        if not kwargs:
            raise ValidationError('No data to update')
        for field in self.instance._meta.fields:
            if field.name not in kwargs:
                kwargs[field.name] = getattr(self.instance, field.name)
        new_instance = self.instance.__class__.objects.create(**funcy.omit(kwargs, 'id'))
        return new_instance

    def archive(self) -> int:
        if not hasattr(self.instance, 'archived'):
            raise FieldDoesNotExist(
                f'{self.instance.__class__.__name__} has no archived field'
            )
        self.instance.archived = True
        self.instance.save()
        return self.instance.pk
