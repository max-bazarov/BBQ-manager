from decimal import Decimal, getcontext

import pytest
from django.test import TestCase

from core.services import ArchiveService
from core.tests import (BaseArchiveServiceTest, BaseCreateServiceTest,
                        BaseDestroyServiceTest)
from employees.models import Employee, MasterProcedure
from procedures.models import Procedure
from purchases.models import UsedMaterial, Purchase, PurchaseProcedure

from .models import Material, MaterialUnits
from .services import MaterialCreateService, MaterialDestroyService
from rest_framework.test import APITestCase

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
            'price': Decimal(10),
        }
        cls.data = {
            'name': 'Hair Color',
            'price': Decimal('1.11'),
            'unit': MaterialUnits.GRAMMS.value
        }

        cls.instance = Material.objects.create(**cls.data)


class TestMaterialDestroyService(APITestCase):

    def __init__(self, methodName: str = ...):
        super().__init__(methodName)
        self.instance = None

    data = {
        'name': 'Hair Color',
        'price': Decimal('1.11'),
        'unit': MaterialUnits.GRAMMS.value
    }

    @classmethod
    def SetUpClass(cls):
        cls.model = Material
        UsedMaterial.objects.create(
            material=cls.data,
            amount=1
        )

    def test_destroy(self):
        count = Material.objects.count()
        MaterialDestroyService(self.instance).destroy()

        assert Material.objects.count() == count - 1, (
            f'{MaterialDestroyService.__name__} does not delete instance after destroy.'
        )