from datetime import datetime
from decimal import Decimal, getcontext

import pytest
from django.test import TestCase
from django.urls import reverse
from mixer.backend.django import mixer
from rest_framework import status
from rest_framework.test import APITestCase

from core.tests import (BaseCRUDArchiveViewTest, NewBaseCreateTestMixin,
                        NewBaseDestroyTestMixin,
                        NewBaseDestroyWithUnarchivedRelationsTestMixin,
                        NewBaseUpdateTestMixin)
from employees.models import Employee, MasterProcedure
from procedures.models import Procedure
from purchases.models import Purchase, PurchaseProcedure, UsedMaterial

from .models import Material, MaterialUnits
from .serializers import MaterialSerializer
from .services import MaterialService


class TestNewMaterialService(TestCase,
                             NewBaseCreateTestMixin,
                             NewBaseUpdateTestMixin,
                             NewBaseDestroyTestMixin,
                             NewBaseDestroyWithUnarchivedRelationsTestMixin):
    model = Material
    service = MaterialService

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.instance = mixer.blend(cls.model)
        cls.instance_with_relation = mixer.blend(cls.model)
        mixer.blend(UsedMaterial, material=cls.instance_with_relation)
        cls.relations_queryset = cls.instance_with_relation.uses.all()
        cls.data = {
            'name': 'some material',
            'unit': MaterialUnits.GRAMMS.value,
            'price': '1.00',
        }
        cls.invalid_data = {'price': 'test'}
        cls.update_data = {
            'name': 'Haircolor'
        }


@pytest.mark.django_db
class TestMaterialView(APITestCase, BaseCRUDArchiveViewTest):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.basename = 'material'
        cls.serializer = MaterialSerializer
        cls.model = Material
        getcontext().prec = 2
        cls.update_data = {
            'name': 'Hair Color 1',
            'price': '1.11',
            'unit': MaterialUnits.GRAMMS.value

        }

        cls.data = {
            'name': 'Hair Color',
            'price': 1.11,
            'unit': MaterialUnits.GRAMMS.value
        }
        cls.instance = Material.objects.create(
            name='zizi',
            price=Decimal('228'),
            unit='GR'
        )
        cls.instance_with_relation = Material.objects.create(
            name='Haircut',
            price=Decimal('220'),
            unit='PC'
        )
        cls.employee = Employee.objects.create(
            first_name='name',
            last_name='surname',
            position='someone',
            coefficient=0.6
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
