from decimal import Decimal, getcontext

import pytest
from django.test import TestCase


from core.services import ArchiveService
from core.tests import (BaseArchiveServiceTest, BaseCreateServiceTest,
                        BaseDestroyServiceTest, BaseCRUDArchiveViewTest)
from purchases.models import UsedMaterial

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
            'price': Decimal(10),
        }
        cls.data = {
            'name': 'Hair Color',
            'price': Decimal('1.11'),
            'unit': MaterialUnits.GRAMMS.value
        }

        cls.instance = Material.objects.create(**cls.data)


@pytest.mark.django_db
class TestMaterialDestroyService(TestCase):


    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.model = Material
        cls.data = {
            'name': 'Hair Color',
            'price': Decimal('1.11'),
            'unit': MaterialUnits.GRAMMS.value
        }
        cls.instance = Material.objects.create(**cls.data)
        UsedMaterial.objects.create(
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
