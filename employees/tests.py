import pytest
from django.test import TestCase
from django.urls import reverse
from mixer.backend.django import mixer
from rest_framework.test import APITestCase

from core.tests import (BaseCreateNestedViewTest, BaseCreateTestMixin,
                        BaseCRUDViewTest, BaseDestroyTestMixin,
                        BaseDestroyWithArchivedRelationsTestMixin,
                        BaseDestroyWithArchivedRelationsViewTest,
                        BaseDestroyWithUnarchivedRelationsTestMixin,
                        BaseDestroyWithUnarchivedRelationsViewTest,
                        BaseListNestedViewTest, BaseSearchViewTest, BaseUpdateDoNothingViewTest,
                        BaseUpdateTestMixin,
                        BaseUpdateWithoutRelationsViewTest,
                        BaseUpdateWithRelationsViewTest)
from employees.models import Employee, MasterProcedure
from employees.serializers import (EmployeeSerializer,
                                   MasterProcedureListSerializer,
                                   MasterProcedureSerializer)
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
        cls.model = Employee
        cls.instance = mixer.blend(cls.model)
        cls.data = {
            'first_name': 'Yakov',
            'last_name': 'Yakov',
            'position': 'CTO',
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
class TestEmployeeViews(APITestCase,
                        BaseCRUDViewTest,
                        BaseCreateNestedViewTest,
                        BaseListNestedViewTest,
                        BaseDestroyWithUnarchivedRelationsViewTest,
                        BaseDestroyWithArchivedRelationsViewTest,
                        BaseUpdateWithoutRelationsViewTest,
                        BaseUpdateWithRelationsViewTest,
                        BaseUpdateDoNothingViewTest,
                        BaseSearchViewTest):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.basename = 'employee'
        cls.model = Employee
        cls.serializer = EmployeeSerializer
        cls.object = mixer.blend(Object)
        cls.instance = mixer.blend(cls.model)
        cls.instance_data = {
            'first_name': cls.instance.first_name
        }
        cls.data = {
            'first_name': 'Yakovv',
            'last_name': 'Varnaevv',
            'position': 'junior developer',
            'object': cls.object.id
        }
        cls.nested_url = reverse('object-employee', args=[cls.object.id])
        cls.update_data = {
            'position': 'senior developer',
            'first_name': 'Yakovv',
            'last_name': 'Varnaevv',
            'object': cls.object.id
        }
        cls.search_fields = [cls.instance.first_name, cls.instance.last_name]
        cls.instance_with_relation = mixer.blend(cls.model)
        mixer.blend(MasterProcedure, employee=cls.instance_with_relation)
        cls.relations_queryset = cls.instance_with_relation.procedures.all()
        cls.nested_queryset = cls.object.employees.all()


class TestMasterProcedureService(TestCase,
                                 BaseCreateTestMixin,
                                 BaseUpdateTestMixin,
                                 BaseDestroyTestMixin,
                                 BaseDestroyWithUnarchivedRelationsTestMixin):

    service = MasterProcedureService

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.model = MasterProcedure
        cls.instance = mixer.blend(cls.model)
        cls.instance_with_relation = mixer.blend(cls.model)
        mixer.blend(PurchaseProcedure, procedure=cls.instance_with_relation)
        cls.data = {
            'employee': mixer.blend(Employee).id,
            'procedure': mixer.blend(Procedure).id,
            'price': '12000.00',
            'coefficient': '0.4'
        }
        cls.update_data = {
            'employee': mixer.blend(Employee).id,
            'procedure': mixer.blend(Procedure).id,
            'price': '9990.00',
            'coefficient': '0.8'
        }
        cls.invalid_data = {'procedure': 'test'}


@pytest.mark.django_db
class TestMasterProcedureViews(APITestCase,
                               BaseCRUDViewTest,
                               BaseDestroyWithUnarchivedRelationsViewTest,
                               BaseUpdateWithoutRelationsViewTest,
                               BaseUpdateWithRelationsViewTest,
                               BaseUpdateDoNothingViewTest,
                               BaseSearchViewTest):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.serializers = {'list': MasterProcedureListSerializer}
        cls.basename = 'master-procedure'
        cls.model = MasterProcedure
        cls.serializer = MasterProcedureSerializer
        cls.instance = mixer.blend(cls.model)
        cls.instance_data = {
            'coefficient': cls.instance.coefficient
        }
        cls.instance_with_relation = mixer.blend(cls.model)
        mixer.blend(PurchaseProcedure, procedure=cls.instance_with_relation)
        cls.data = {
            'employee': mixer.blend(Employee).id,
            'procedure': mixer.blend(Procedure).id,
            'price': '12000.00',
            'coefficient': '0.4'
        }
        cls.update_data = {
            'employee': mixer.blend(Employee).id,
            'procedure': mixer.blend(Procedure).id,
            'price': '9990.00',
            'coefficient': '0.8'
        }
        cls.search_fields = [
            cls.instance.procedure.name,
            cls.instance.employee.first_name,
            cls.instance.employee.last_name
        ]