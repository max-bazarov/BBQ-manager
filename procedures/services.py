from django import forms
from service_objects.services import Service

from core.services import ModelCreateService, ModelDestroyService
from employees.models import MasterProcedure

from .models import Procedure


class ProcedureServiceFields(Service):
    name = forms.CharField(max_length=255)


class ProcedureCreateService(ModelCreateService, ProcedureServiceFields):
    model = Procedure


class ProcedureService:

    def __init__(self, instance, **kwargs):
        self.instance = instance
        self.model = instance.__class__
        self.kwargs = kwargs

    @property
    def has_related(self) -> bool:
        return MasterProcedure.objects.filter(procedure__id=self.instance.id).exists()

    def destroy(self):
        if self.has_related:
            raise Exception(
                f'Procedure with id {self.instance.id} cannot be deleted, because'
                'it has related master procedures.'
            )
        self.model.objects.get(id=self.instance.id).delete()
