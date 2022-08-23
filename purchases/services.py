from core.services import ModelCreateService, ModelDestroyService
from service_objects.services import Service
from django import forms

from .models import UsedMaterial


class BaseUsedMaterialService(Service):
    material = forms.IntegerField()
    procedure = forms.IntegerField()
    amount = forms.IntegerField()

class UsedMaterialCreateService(ModelCreateService, BaseUsedMaterialService):
    model = UsedMaterial

class UsedMaterialDestroyService(ModelDestroyService):
    model = UsedMaterial
