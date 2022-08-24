from typing import Optional

from .models import UsedMaterial


class UsedMaterialService:

    def __init__(self, instance: Optional[UsedMaterial] = None, **kwargs):
        self.instance = instance
        self.model = UsedMaterial
        self.kwargs = kwargs

    def destroy(self):
        self.model.objects.get(id=self.instance.id).delete()

    def create(self) -> UsedMaterial:
        return self.model.objects.get_or_create(**self.kwargs)[0]
