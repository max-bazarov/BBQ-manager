from datetime import datetime
from decimal import Decimal

from mixer.backend.django import mixer
import pytest
from django.test import TestCase
from rest_framework.test import APITestCase

from core.tests import (BaseCRUDViewTest,
                        BaseCreateTestMixin,
                        BaseDestroyTestMixin,
                        BaseUpdateTestMixin)
from employees.models import Employee, MasterProcedure
from inventory.models import Material, MaterialUnits
from procedures.models import Procedure

from .models import Purchase, PurchaseProcedure, UsedMaterial
from .serializers import UsedMaterialSerializer
from .services import UsedMaterialService


class TestUsedMaterialService(TestCase,
                              BaseCreateTestMixin,
                              BaseDestroyTestMixin,
                              BaseUpdateTestMixin):
    model = UsedMaterial
    service = UsedMaterialService

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.instance = mixer.blend(cls.model)
        cls.data = {
            'amount': 1,
            'material': mixer.blend(Material).id,
            'procedure': mixer.blend(PurchaseProcedure).id,
        }
        cls.update_data = {
            'amount': 2,
            'material': mixer.blend(Material).id,
            'procedure': mixer.blend(PurchaseProcedure).id,
        }
        cls.invalid_data = {'material': 'test'}


@pytest.mark.django_db
class TestUsedMaterialViews(APITestCase, BaseCRUDViewTest):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.serializer = UsedMaterialSerializer
        cls.model = UsedMaterial
        cls.basename = 'uses'
        cls.procedure_with_master = Procedure.objects.create(name='master procedure')
        cls.employee = Employee.objects.create(
            first_name='Max',
            last_name='Bazarov',
            position='Boss',
            coefficient=1
        )
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
        cls.material = Material.objects.create(
            name='Hair Color',
            price=Decimal('1.11'),
            unit=MaterialUnits.GRAMMS.value
        )
        cls.data = {
            'procedure': cls.purchase_procedure.id,
            'material': cls.material.id,
            'amount': 2
        }
        cls.update_data = {
            'procedure': cls.purchase_procedure.id,
            'material': cls.material.id,
            'amount': 3
        }
        cls.instance = UsedMaterial.objects.create(
            procedure=cls.purchase_procedure,
            material=cls.material,
            amount=1
        )
