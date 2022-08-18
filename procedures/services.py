from django.db.models import Model
from service_objects.services import Service
from django import forms

from core.services import ModelCreateService, ModelDestroyService

from .models import Procedure


class ProcedureServiceFields(Service):
    name = forms.CharField(max_length=255)


class ProcedureCreateService(ModelCreateService, ProcedureServiceFields):
    model = Procedure


class ProcedureDestroyService(ModelDestroyService):
    model = Procedure
