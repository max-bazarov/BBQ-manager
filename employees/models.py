from django.db import models


class Employee(models.Model):

    class Meta:
        db_table = 'employees'

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    coeffitient = models.FloatField()


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
    coeffitient = models.FloatField()
    archived = models.BooleanField(default=False)
