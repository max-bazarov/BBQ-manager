from django import forms
from service_objects.services import Service

from core.services import ModelCreateService, ModelDestroyService

from .models import Procedure


class ProcedureServiceFields(Service):
    name = forms.CharField(max_length=255)


class ProcedureCreateService(ModelCreateService, ProcedureServiceFields):
    model = Procedure


class ProcedureDestroyService(ModelDestroyService):
    model = Procedure
