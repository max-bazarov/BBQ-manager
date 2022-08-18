from django import forms
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
