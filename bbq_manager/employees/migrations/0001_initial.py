# Generated by Django 4.1 on 2022-09-03 17:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('procedures', '0001_initial'),
        ('objects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('position', models.CharField(max_length=255)),
                ('archived', models.BooleanField(default=False)),
                ('object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='objects.object')),
            ],
            options={
                'db_table': 'employees',
            },
        ),
        migrations.CreateModel(
            name='MasterProcedure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('coefficient', models.FloatField()),
                ('archived', models.BooleanField(default=False)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='procedures', to='employees.employee')),
                ('procedure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='procedures.procedure')),
            ],
            options={
                'db_table': 'master_procedure',
            },
        ),
    ]