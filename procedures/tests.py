from decimal import Decimal

import pytest
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.tests import BaseCreateServiceTest, BaseCRUDViewTest
from employees.models import Employee, MasterProcedure
from procedures.serializers import ProcedureSerializer

from .models import Procedure
from .serializers import ProcedureSerializer
from .services import ProcedureCreateService, ProcedureService


@pytest.mark.django_db
class TestProcedureServices(TestCase, BaseCreateServiceTest):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.model = Procedure
        cls.create_service = ProcedureCreateService

        cls.data = {
            'name': 'test'
        }
        cls.instance = Procedure.objects.create(**cls.data)
        cls.procedure_with_master = Procedure.objects.create(name='master procedure')
        cls.employee = Employee.objects.create(
            first_name='name',
            last_name='surname',
            position='someone',
            coeffitient=1.11
        )
        MasterProcedure.objects.create(
            procedure=cls.procedure_with_master,
            employee=cls.employee,
            price=Decimal(1),
            coeffitient=0.5,
        )

    def test_destroy_without_master_procedures(self):
        count = Procedure.objects.count()

        ProcedureService(self.instance).destroy()

        assert Procedure.objects.count() == count - 1, (
            f'{ProcedureService.__name__} does not delete instance after destroy.'
        )

    def test_destroy_with_master_procedure(self):
        count = Procedure.objects.count()

        try:
            ProcedureService(self.procedure_with_master).destroy()
        except Exception:
            pass
        else:
            assert False, (
                f'{ProcedureService.__name__} should raise exception if destroying procedure has '
                'related objects.'
            )
        assert Procedure.objects.count() == count, (
            f'{ProcedureService.__name__} should not delete instance if it has related objects.'
        )


@pytest.mark.django_db
class TestProcedureViews(APITestCase, BaseCRUDViewTest):
    model = Procedure
    serializer = ProcedureSerializer
    basename = 'procedure'

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.data = {
            'name': 'test'
        }
        cls.update_data = {
            'name': 'new test'
        }

        cls.instance = Procedure.objects.create(name='instance')
        cls.procedure_with_master = Procedure.objects.create(name='master procedure')
        cls.employee = Employee.objects.create(
            first_name='name',
            last_name='surname',
            position='someone',
            coeffitient=1.11
        )
        MasterProcedure.objects.create(
            procedure=cls.procedure_with_master,
            employee=cls.employee,
            price=Decimal(1),
            coeffitient=0.5,
        )

    def test_delete_without_master(self):
        count = Procedure.objects.count()
        url = reverse('procedure-detail', args=[self.instance.id])
        response = self.client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert count - 1 == Procedure.objects.count()
