from decimal import Decimal, getcontext

import pytest
from django.test import TestCase

from core.tests import BaseCreateServiceTest, BaseDestroyServiceTest

from .models import Material, MaterialUnits
from .services import MaterialCreateService, MaterialDestroyService


@pytest.mark.django_db
class TestMaterialCreateService(TestCase,
                                BaseCreateServiceTest,
                                BaseDestroyServiceTest):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.model = Material
        cls.create_service = MaterialCreateService
        cls.destroy_service = MaterialDestroyService

        getcontext().prec = 2
        cls.data = {
            'name': 'Hair Color',
            'price': Decimal('1.11'),
            'unit': MaterialUnits.GRAMMS.value
        }
        cls.instance = Material.objects.create(**cls.data)
