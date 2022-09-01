# Generated by Django 4.1 on 2022-09-01 19:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0002_null_parent'),
        ('employees', '0005_employee_object'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='object',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='objects.object'),
        ),
    ]
