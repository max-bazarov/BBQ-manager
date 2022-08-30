from django.db import models


class MaterialUnits(models.TextChoices):
    GRAMMS = 'GR', 'Gramms'
    PIECES = 'PC', 'Pieces'


class Material(models.Model):

    class Meta:
        db_table = 'materials'

    name = models.CharField('material_name', max_length=255)
    unit = models.CharField(
        'material_measurment_units',
        max_length=3,
        choices=MaterialUnits.choices
    )
    archived = models.BooleanField(
        'is_archived',
        default=False
    )
    object = models.ForeignKey(
        'objects.Object',
        on_delete=models.CASCADE,
        related_name='materials'
    )

    def __str__(self):
        return self.name


class Stock(models.Model):

    class Meta:
        db_table = 'stocks'

    price = models.DecimalField(
        'material_price',
        max_digits=10,
        decimal_places=2,
    )
    material = models.ForeignKey(
        Material,
        on_delete=models.PROTECT,
        related_name='stock'
    )
    amount = models.IntegerField(default=1)


class ProductMaterial(models.Model):

    class Meta:
        db_table = 'product_material'

    material = models.ForeignKey(
        Material,
        on_delete=models.PROTECT,
        related_name='product_materials'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    archived = models.BooleanField(
        'is_archived',
        default=False
    )
