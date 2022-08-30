import pytest
from django.test import TestCase
from mixer.backend.django import mixer
from rest_framework.test import APITestCase

from core.tests import (BaseCreateTestMixin, BaseCRUDViewTest,
                        BaseDestroyTestMixin, BaseUpdateTestMixin)
from inventory.models import Material, ProductMaterial

from .models import PurchaseProcedure, UsedMaterial
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
            'material': mixer.blend(ProductMaterial).id,
            'procedure': mixer.blend(PurchaseProcedure).id,
        }
        cls.update_data = {
            'amount': 2,
            'material': mixer.blend(ProductMaterial).id,
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
        cls.product_material = mixer.blend(ProductMaterial)
        cls.purchase_procedure = mixer.blend(PurchaseProcedure)
        cls.data = {
            'procedure': cls.purchase_procedure.id,
            'material': cls.product_material.id,
            'amount': 2
        }
        cls.update_data = {
            'procedure': cls.purchase_procedure.id,
            'material': cls.product_material.id,
            'amount': 3
        }
        cls.instance = mixer.blend(UsedMaterial)
