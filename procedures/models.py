from django.db import models


class Procedure(models.Model):

    class Meta:
        db_table = 'precedures'

    name = models.CharField('Procedure_name', max_length=255)
    archived = models.BooleanField(default=False)
    department = models.ForeignKey(
        'objects.Department',
        on_delete=models.CASCADE,
        related_name='procedures'
    )

    def __str__(self) -> str:
        return f'{self.name} at {self.department}'
