import pytest

from django.test import TestCase

from core.tests import BaseCreateServiceTests
from .models import Material, MaterialUnits
from .services import MaterialServiceCreate


@pytest.mark.django_db
class TestMaterialCreateService(TestCase, BaseCreateServiceTests):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.model = Material
        cls.create_service = MaterialServiceCreate
        cls.data = {
            'name': 'Hair Color',
            'price': 1.11,
            'unit': MaterialUnits.GRAMMS.value
        }
