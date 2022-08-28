from django.db import models


class Company(models.Model):

    class Meta:
        db_table = 'companies'

    name = models.CharField('company_name', max_length=255)

    def __str__(self) -> str:
        return self.name


class Object(models.Model):

    class Meta:
        db_table = 'objects'

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='objects'
    )
    address = models.CharField('object_address', max_length=255)

    def __str__(self) -> str:
        return f'{self.company.name} on {self.address}'


class Department(models.Model):

    class Meta:
        db_table = 'departments'

    name = models.CharField('department_name', max_length=255)
    parent = models.ForeignKey(
        'Department',
        on_delete=models.CASCADE,
        related_name='child_departments',
        blank=True,
        null=True
    )
    object = models.ForeignKey(
        Object,
        on_delete=models.CASCADE,
        related_name='departments'
    )

    def __str__(self) -> str:
        return self.name
