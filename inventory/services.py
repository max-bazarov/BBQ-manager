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


class MaterialDestroyService:
    def __init__(self, instance):
        self.instance = instance
        self.model = instance.__class__
        
    def has_related(self) -> bool:
        return self.instance.uses.exists()

    def destroy(self):
        if self.has_related():
            raise Exception(
                f'Material cannot be deleted, because it is used material'
            )
        self.instance.delete()
