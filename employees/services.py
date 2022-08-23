from .models import Employee


class EmployeeService:

    def __init__(self, instance: Employee) -> None:
        self.instance = instance
        self.model = instance.__class__

    def has_related(self) -> bool:
        return self.instance.procedures.exists()

    def destroy(self):
        if self.has_related():
            raise Exception(
                f'Employee with id {self.instance.id} cannot be deleted.'
                'Because there are related instances.'
            )
        self.model.objects.get(id=self.instance.id).delete()
        return self.instance.id
