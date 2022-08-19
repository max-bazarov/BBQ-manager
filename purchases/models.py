from django.db import models


class Purchase(models.Model):

    class Meta:
        db_table = 'procedure_purchases'

    time = models.DateTimeField()
    procedure = models.ForeignKey('employees.MasterProcedure', on_delete=models.DO_NOTHING)
    is_paid_by_card = models.BooleanField(default=False)