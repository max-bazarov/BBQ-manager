import pytest

from django.test import TestCase

from core.tests import BaseCreateServiceTest, BaseDestroyServiceTest
from .models import Procedure
from .services import ProcedureCreateService, ProcedureDestroyService


@pytest.mark.django_db
class TestProcedureServices(TestCase, BaseCreateServiceTest, BaseDestroyServiceTest):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.model = Procedure
        cls.create_service = ProcedureCreateService
        cls.destroy_service = ProcedureDestroyService

        cls.data = {
            'name': 'test'
        }
        cls.instance = Procedure.objects.create(**cls.data)
