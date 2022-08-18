import funcy
from django import forms
from django.db.models import Model
from service_objects.services import Service

from core.services import ModelCreateService, ModelDestroyService

from .models import Material


class BaseMaterialService(Service):
    name = forms.CharField(max_length=255)
    unit = forms.CharField(max_length=2)
    price = forms.DecimalField(decimal_places=2)
    archived = forms.BooleanField(required=False, initial=False)


class MaterialCreateService(ModelCreateService, BaseMaterialService):
    model = Material


class MaterialDestroyService(ModelDestroyService):
    model = Material


class ArchiveModelService:

    def __init__(self, instance: Model) -> None:
        self.instance = instance

    def update(self, **kwargs: dict[str, type[Model]]) -> Model:
        self.archive()
        for field in funcy.omit(self.instance._meta.fields, 'id'):
            if field.name not in kwargs:
                kwargs[field.name] = getattr(self.instance, field.name)
        new_instance = self.instance.__class__.objects.create(**kwargs)
        return new_instance

    def archive(self) -> int:
        self.instance.archived = True
        self.instance.save()
        return self.instance.pk
