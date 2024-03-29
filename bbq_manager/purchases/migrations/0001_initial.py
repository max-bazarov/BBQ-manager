# Generated by Django 4.1 on 2022-09-03 17:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inventory', '0001_initial'),
        ('employees', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('is_paid_by_card', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'procedure_purchases',
            },
        ),
        migrations.CreateModel(
            name='PurchaseProcedure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('procedure', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='employees.masterprocedure')),
                ('purchase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purchases.purchase')),
            ],
            options={
                'db_table': 'purchase_procedure',
            },
        ),
        migrations.CreateModel(
            name='UsedMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=1)),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='materials', to='inventory.productmaterial')),
                ('procedure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='procedures', to='purchases.purchaseprocedure')),
            ],
            options={
                'db_table': 'used_materials',
            },
        ),
        migrations.AddField(
            model_name='purchase',
            name='procedures',
            field=models.ManyToManyField(related_name='purchases', through='purchases.PurchaseProcedure', to='employees.masterprocedure'),
        ),
    ]
