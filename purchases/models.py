from django.db import models


class Purchase(models.Model):

    class Meta:
        db_table = 'procedure_purchases'

    time = models.DateTimeField(auto_now_add=True)
    is_paid_by_card = models.BooleanField(default=False)


class PurchaseProcedure(models.Model):

    class Meta:
        db_table = 'purchase_procedure'

    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    procedure = models.ForeignKey('employees.MasterProcedure', on_delete=models.DO_NOTHING)


class UsedMaterial(models.Model):

    material = models.ForeignKey(
        'inventory.ProductMaterial',
        on_delete=models.PROTECT,
        related_name='uses'
    )
    procedure = models.ForeignKey(
        PurchaseProcedure,
        on_delete=models.CASCADE,
        related_name='materials',
    )
    amount = models.IntegerField(default=1)
