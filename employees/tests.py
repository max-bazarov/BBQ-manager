import pytest
from django.test import TestCase
from django.urls import reverse
from mixer.backend.django import mixer
from rest_framework.test import APITestCase

from core.tests import (BaseCreateNestedViewTest, BaseCreateTestMixin,
                        BaseCRUDViewTest, BaseDestroyTestMixin,
                        BaseDestroyWithArchivedRelationsTestMixin,
                        BaseDestroyWithUnarchivedRelationsTestMixin,
                        BaseUpdateTestMixin)
from employees.models import Employee, MasterProcedure
from employees.serializers import EmployeeSerializer
from employees.services import EmployeeService, MasterProcedureService
from objects.models import Object
from procedures.models import Procedure
from purchases.models import PurchaseProcedure


class TestEmployeeService(TestCase,
                          BaseCreateTestMixin,
                          BaseUpdateTestMixin,
                          BaseDestroyTestMixin,
                          BaseDestroyWithArchivedRelationsTestMixin,
                          BaseDestroyWithUnarchivedRelationsTestMixin):
    model = Employee
    service = EmployeeService

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.instance = mixer.blend(cls.model)
        cls.data = {
            'first_name': 'Yakov',
            'last_name': 'Yakov',
            'position': 'CTO',
            'coefficient': '0.82',
            'object': cls.instance.object.id
        }
        cls.invalid_data = {
            'last_name': 52
        }
        cls.update_data = {
            'position': 'Senior Backend Developer'
        }
        cls.instance_with_relation = mixer.blend(cls.model)
        mixer.blend(MasterProcedure, employee=cls.instance_with_relation)
        cls.relations_queryset = cls.instance_with_relation.procedures.all()


@pytest.mark.django_db
class TestEmployeeViews(APITestCase, BaseCreateNestedViewTest, BaseCRUDViewTest):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.basename = 'employee'
        cls.model = Employee
        cls.serializer = EmployeeSerializer
        cls.object = mixer.blend(Object)
        cls.data = {
            'first_name': 'Yakovv',
            'last_name': 'Varnaevv',
            'position': 'junior developer',
            'coefficient': 0.5,
            'object': cls.object.id
        }
        cls.nested_url = reverse('object-employee', args=[cls.object.id])
        cls.update_data = {
            'position': 'senior developer',
            'first_name': 'Yakovv',
            'last_name': 'Varnaevv',
            'coefficient': 0.5,
            'object': cls.object.id
        }
        cls.instance = mixer.blend(Employee)


class TestMasterProcedureService(TestCase,
                                 BaseCreateTestMixin,
                                 BaseDestroyTestMixin,
                                 BaseDestroyWithUnarchivedRelationsTestMixin):
    model = MasterProcedure
    service = MasterProcedureService

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.instance = mixer.blend(cls.model)
        cls.instance_with_relation = mixer.blend(cls.model)
        mixer.blend(PurchaseProcedure, procedure=cls.instance_with_relation)
        cls.data = {
            'employee': mixer.blend(Employee).id,
            'procedure': mixer.blend(Procedure).id,
            'price': '12000.00',
            'coefficient': 0.4
        }
        cls.invalid_data = {'procedure': 'test'}
        cls.relations_queryset = cls.instance_with_relation.purchases.all()
