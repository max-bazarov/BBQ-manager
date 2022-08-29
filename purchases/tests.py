from datetime import datetime
from decimal import Decimal

import pytest
from django.test import TestCase
from mixer.backend.django import mixer
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
        cls.basename = 'used-material'
        cls.material = mixer.blend(Material)
        cls.purchase_procedure = mixer.blend(PurchaseProcedure)
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
        cls.instance = mixer.blend(UsedMaterial)
