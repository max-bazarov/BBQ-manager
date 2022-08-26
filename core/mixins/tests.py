from django.db.models import ManyToManyField, Model


class BaseTestsUtilMixin:
    model: type[Model]
    isntance: Model

    def get_count(self) -> int:
        return self.model.objects.count()

    def get_instance(self, id) -> Model:
        return self.model.objects.get(id=id)

    def is_isntance_exists(self, **kwargs) -> bool:
        return self.model.objects.filter(**kwargs).exists()

    def get_instance_data(self) -> dict:
        data = {}
        for f in self.instance._meta.fields:
            if isinstance(f, ManyToManyField):
                continue
            data[f.name] = getattr(self.instance, f.name)
        return data
