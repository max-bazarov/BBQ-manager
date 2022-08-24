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
    price = models.DecimalField(
        'material_price',
        max_digits=10,
        decimal_places=2,
    )
    archived = models.BooleanField(
        'is_archived',
        default=False
    )

    def __str__(self):
        return self.name
