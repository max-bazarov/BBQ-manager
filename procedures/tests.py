import pytest

from django.test import TestCase

from core.tests import BaseCreateServiceTests
from .models import Procedure
from .services import ProcedureCreateService


@pytest.mark.django_db
class TestProcedureServices(TestCase, BaseCreateServiceTests):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.model = Procedure
        cls.create_service = ProcedureCreateService

        cls.data = {
            'name': 'test'
        }
