from typing import Optional

from django import forms
from service_objects.services import Service

from .models import Material


class MaterialServiceCreate(Service):
    name = forms.CharField(max_length=255)
    unit = forms.CharField(max_length=2)
    price = forms.DecimalField(decimal_places=2)
    archived = forms.BooleanField(required=False, initial=False)

    def process(self) -> Material:
        return Material.objects.create(**self.cleaned_data)
        
