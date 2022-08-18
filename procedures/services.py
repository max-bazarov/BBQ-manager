from service_objects.services import Service
from django import forms

from .models import Procedure


class ProcedureServiceFields:
    name = forms.CharField(max_length=255)


class ProcedureCreateService(Service, ProcedureServiceFields):

    def process(self):
        return Procedure.objects.create(**self.cleaned_data)

