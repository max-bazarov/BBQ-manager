from django.db import models


class Purchase(models.Model):

    class Meta:
        db_table = 'procedure_purchases'

    time = models.DateTimeField(auto_now_add=True)
    is_paid_by_card = models.BooleanField(default=False)
    procedures = models.ManyToManyField(
        'employees.MasterProcedure',
        related_name='procedures',
        through='PurchaseProcedure'
    )


class PurchaseProcedure(models.Model):

    class Meta:
        db_table = 'purchase_procedure'

    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    procedure = models.ForeignKey('employees.MasterProcedure', on_delete=models.DO_NOTHING)


class UsedMaterial(models.Model):

    procedure = models.ForeignKey(
        PurchaseProcedure,
        on_delete=models.CASCADE,
        related_name='materials', blank=True, null=True,
    )
    material = models.ForeignKey(
        'inventory.Material',
        on_delete=models.DO_NOTHING,
        related_name='uses'
    )
    amount = models.IntegerField(default=1)
