from datetime import datetime
from decimal import Decimal, getcontext

import pytest
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.services import ArchiveService
from core.tests import (BaseArchiveServiceTest, BaseCreateServiceTest,
                        BaseCRUDArchiveViewTest)
from employees.models import Employee, MasterProcedure
from procedures.models import Procedure
from purchases.models import Purchase, PurchaseProcedure, UsedMaterial

from .models import Material, MaterialUnits
from .serializers import MaterialSerializer
from .services import MaterialCreateService, MaterialDestroyService


@pytest.mark.django_db
class TestMaterialService(TestCase,
                          BaseCreateServiceTest,
                          BaseArchiveServiceTest):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.model = Material
        cls.create_service = MaterialCreateService
        cls.archive_service = ArchiveService

        getcontext().prec = 2
        cls.update_data = {
            'price': Decimal('12131.11'),
        }
        cls.data = {
            'name': 'Hair Color',
            'price': Decimal('1.11'),
            'unit': MaterialUnits.GRAMMS.value
        }

        cls.instance = Material.objects.create(
            name='Haircut',
            price=220,
            unit='PC'
        )
        cls.employee = Employee.objects.create(
            first_name='name',
            last_name='surname',
            position='someone',
            coefficient=1.11
        )
        cls.procedure_with_master = Procedure.objects.create(name='master procedure')
        cls.master_procedure = MasterProcedure.objects.create(
            procedure=cls.procedure_with_master,
            employee=cls.employee,
            price=Decimal(1),
            coefficient=0.5,
        )
        cls.purchase = Purchase.objects.create(
            time=datetime.now(),
            is_paid_by_card=False,
        )
        cls.purchase_procedure = PurchaseProcedure.objects.create(
            purchase=cls.purchase,
            procedure=cls.master_procedure
        )
        UsedMaterial.objects.create(
            procedure=cls.purchase_procedure,
            material=cls.instance,
            amount=1
        )

    def test_destroy(self):
        count = Material.objects.count()
        try:
            MaterialDestroyService(self.instance).destroy()
        except Exception:
            pass
        else:
            assert False, ('Service must raise exception.')

        assert Material.objects.count() == count, (
            f'{MaterialDestroyService.__name__} does not delete instance after destroy.'
        )


@pytest.mark.django_db
class TestMaterialView(APITestCase,
                       BaseCRUDArchiveViewTest):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.basename = 'material'
        cls.serializer = MaterialSerializer
        cls.model = Material
        getcontext().prec = 2
        cls.update_data = {
            'price': 1.11,
            'unit': MaterialUnits.GRAMMS.value
        }
        cls.update_data_without_changes = {

            'price': 228,
            # 'unit': MaterialUnits.GRAMMS.value
        }
        cls.data = {
            'name': 'Hair Color',
            'price': 1.11,
            'unit': MaterialUnits.GRAMMS.value
        }
        cls.instance = Material.objects.create(
            name='zizi',
            price=228,
            unit='GR'
        )
        cls.instance_with_relation = Material.objects.create(
            name='Haircut',
            price=220,
            unit='PC'
        )
        cls.employee = Employee.objects.create(
            first_name='name',
            last_name='surname',
            position='someone',
            coefficient=1.11
        )
        cls.procedure_with_master = Procedure.objects.create(name='master procedure')
        cls.master_procedure = MasterProcedure.objects.create(
            procedure=cls.procedure_with_master,
            employee=cls.employee,
            price=Decimal(1),
            coefficient=0.5,
        )
        cls.purchase = Purchase.objects.create(
            time=datetime.now(),
            is_paid_by_card=False,
        )
        cls.purchase_procedure = PurchaseProcedure.objects.create(
            purchase=cls.purchase,
            procedure=cls.master_procedure
        )
        UsedMaterial.objects.create(
            procedure=cls.purchase_procedure,
            material=cls.instance_with_relation,
            amount=1
        )

    def test_destroy_view_with_relation(self):
        count = self.model.objects.count()
        url = reverse(self.basename + '-detail', args=[self.instance_with_relation.id])
        response = self.client.delete(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert count == self.model.objects.count()

    def test_update_view_without_changes(self):
        count = self.model.objects.count()
        url = reverse(self.basename + '-detail', args=[self.instance.id])
        response = self.client.put(url, self.update_data_without_changes)

        assert response.status_code == status.HTTP_400_BAD_REQUEST, str(response.json())
        assert count == self.model.objects.count()
        assert self.model.objects.filter(id=self.instance.id).exists()
        assert self.model.objects.get(id=self.instance.id).archived
        assert response.json() == self.serializer(self.model.objects.last()).data