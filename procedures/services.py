from typing import Optional

from django import forms
from service_objects.services import Service

from employees.models import MasterProcedure

from .models import Procedure


class ProcedureServiceFields(Service):
    name = forms.CharField(max_length=255)


class ProcedureService:

    def __init__(self, instance: Optional[Procedure] = None, **kwargs):
        self.instance = instance
        self.model = Procedure
        self.kwargs = kwargs

    def has_related(self) -> bool:
        return MasterProcedure.objects.filter(procedure__id=self.instance.id).exists()

    def destroy(self):
        if self.has_related():
            raise Exception(
                f'Procedure with id {self.instance.id} cannot be deleted, because'
                'it has related master procedures.'
            )
        self.model.objects.get(id=self.instance.id).delete()

    def create(self) -> Procedure:
        return self.model.objects.get_or_create(**self.kwargs)[0]
