from django import forms
from service_objects.services import Service


class ModelCreateService:

    def process(self):
        return self.model.objects.create(**self.cleaned_data)

    class Meta:
        abstract = True


class ModelDestroyService(Service):
    id = forms.IntegerField()

    def process(self):
        self.model.objects.filter(**self.cleaned_data).delete()
