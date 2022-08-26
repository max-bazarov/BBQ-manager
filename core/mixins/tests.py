from django.db.models import ManyToManyField, Model


class BaseTestsUtilMixin:
    model: type[Model]
    instance: Model

    def get_count(self) -> int:
        return self.model.objects.count()

    def get_instance(self, id) -> Model:
        return self.model.objects.get(id=id)

    def is_instance_exists(self, **kwargs) -> bool:
        return self.model.objects.filter(**kwargs).exists()

    def get_instance_data(self) -> dict:
        data = {}
        for f in self.instance._meta.fields:
            if isinstance(f, ManyToManyField):
                continue
            data[f.name] = getattr(self.instance, f.name)
        return data
