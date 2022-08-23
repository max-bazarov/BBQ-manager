from decimal import Decimal

import pytest
from django.test import TestCase
from rest_framework.test import APITestCase

from core.tests import (BaseCRUDViewTest,
                        DestroyInstancesWithRelationalDependenciesTestMixin)
from employees.models import Employee, MasterProcedure
from employees.serializers import EmployeeSerializer
from employees.services import EmployeeService
from procedures.models import Procedure


class TestEmployeeDestroyService(TestCase,
                                 DestroyInstancesWithRelationalDependenciesTestMixin):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.model = Employee
        cls.destroy_service = EmployeeService
        cls.instance = Employee.objects.create(
            first_name='Yakov',
            last_name='Varnaev',
            position='developer',
            coefficient=0.5
        )
        cls.instance_with_relation = Employee.objects.create(
            first_name='Yakovv',
            last_name='Varnaevv',
            position='developerr',
            coefficient=0.5
        )
        cls.procedure_with_master = Procedure.objects.create(name='master procedure')
        MasterProcedure.objects.create(
            procedure=cls.procedure_with_master,
            employee=cls.instance_with_relation,
            price=Decimal(1),
            coefficient=0.5
        )


@pytest.mark.django_db
class TestEmployeeViews(APITestCase, BaseCRUDViewTest):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.basename = 'employee'
        cls.model = Employee
        cls.serializer = EmployeeSerializer
        cls.data = {
            'first_name': 'Yakovv',
            'last_name': 'Varnaevv',
            'position': 'junior developer',
            'coefficient': 0.5
        }
        cls.update_data = {
            'position': 'senior developer',
            'first_name': 'Yakovv',
            'last_name': 'Varnaevv',
            'coefficient': 0.5
        }
        cls.instance = Employee.objects.create(
            first_name='Yakov',
            last_name='Varnaev',
            position='developer',
            coefficient=0.5
        )
