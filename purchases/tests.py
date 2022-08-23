import pytest
from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from datetime import datetime

from core.tests import BaseCRUDViewTest, BaseCreateServiceTest, BaseDestroyServiceTest
from employees.models import Employee, MasterProcedure
from procedures.models import Procedure
from procedures.serializers import ProcedureSerializer
from inventory.models import Material, MaterialUnits

from .models import UsedMaterial, Purchase, PurchaseProcedure
from .services import UsedMaterialCreateService, UsedMaterialDestroyService
from .serializers import UsedMaterialSerializer


@pytest.mark.django_db
class TestUsedMaterialService(TestCase, BaseCreateServiceTest, BaseDestroyServiceTest):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.model = UsedMaterial
        cls.create_service = UsedMaterialCreateService
        cls.destroy_service = UsedMaterialDestroyService

        cls.employee = Employee.objects.create(
            first_name='name',
            last_name='surname',
            position='someone',
            coeffitient=1.11
        )
        cls.procedure_with_master = Procedure.objects.create(name='master procedure')
        cls.master_procedure = MasterProcedure.objects.create(
            procedure=cls.procedure_with_master,
            employee=cls.employee,
            price=Decimal(1),
            coeffitient=0.5,
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
        cls.instance = UsedMaterial.objects.create(
            procedure=cls.purchase_procedure.id,
            material=cls.material.id,
            amount=1
        )
