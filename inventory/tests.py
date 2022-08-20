from decimal import Decimal, getcontext

import pytest
from django.test import TestCase

from core.services import ArchiveService
from core.tests import (BaseArchiveServiceTest, BaseCreateServiceTest,
                        BaseDestroyServiceTest)

from .models import Material, MaterialUnits
from .services import MaterialCreateService, MaterialDestroyService


@pytest.mark.django_db
class TestMaterialService(TestCase,
                          BaseCreateServiceTest,
                          BaseDestroyServiceTest,
                          BaseArchiveServiceTest):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.model = Material
        cls.create_service = MaterialCreateService
        cls.destroy_service = MaterialDestroyService
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
