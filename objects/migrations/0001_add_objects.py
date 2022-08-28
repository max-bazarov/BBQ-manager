# Generated by Django 4.1 on 2022-08-28 17:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='company_name')),
            ],
            options={
                'db_table': 'companies',
            },
        ),
        migrations.CreateModel(
            name='Object',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=255, verbose_name='object_address')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='objects', to='objects.company')),
            ],
            options={
                'db_table': 'objects',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='department_name')),
                ('object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departments', to='objects.object')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='child_departments', to='objects.department')),
            ],
            options={
                'db_table': 'departments',
            },
        ),
    ]
