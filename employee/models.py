from django.db import models


class Employee(models.Model):

    class Meta:
        db_table = 'employees'

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
