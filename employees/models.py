from django.db import models


class Employee(models.Model):

    class Meta:
        db_table = 'employees'

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    coefficient = models.FloatField()

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class MasterProcedure(models.Model):

    class Meta:
        db_table = 'master_procedure'

    procedure = models.ForeignKey(
        'procedures.Procedure',
        on_delete=models.CASCADE,
        related_name='employees',
    )
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='procedures',
    )
    price = models.DecimalField(
        decimal_places=2,
        max_digits=7,
    )
    coefficient = models.FloatField()
    archived = models.BooleanField(default=False)

    def __str__(self):
        return self.procedure.name
