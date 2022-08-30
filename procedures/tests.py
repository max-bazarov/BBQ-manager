import pytest
from django.test import TestCase
from mixer.backend.django import mixer
from rest_framework.test import APITestCase

from core.tests import (BaseCreateTestMixin, BaseCRUDViewTest,
                        BaseDestroyTestMixin,
                        BaseDestroyWithArchivedRelationsTestMixin,
                        BaseDestroyWithArchivedRelationsViewTest,
                        BaseDestroyWithUnarchivedRelationsTestMixin,
                        BaseDestroyWithUnarchivedRelationsViewTest,
                        BaseUpdateTestMixin,
                        BaseUpdateWithoutRelationsViewTest,
                        BaseUpdateWithRelationsViewTest,
                        BaseUpdateDoNothingViewTest)

from employees.models import MasterProcedure
from objects.models import Department

from .models import Procedure
from .serializers import ProcedureSerializer
from .services import ProcedureService


@pytest.mark.django_db
class TestProcedureService(TestCase,
                           BaseCreateTestMixin,
                           BaseUpdateTestMixin,
                           BaseDestroyTestMixin,
                           BaseDestroyWithArchivedRelationsTestMixin,
                           BaseDestroyWithUnarchivedRelationsTestMixin):
    model = Procedure
    service = ProcedureService

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.instance = mixer.blend(cls.model)
        cls.instance_with_relation = mixer.blend(cls.model)
        mixer.blend(MasterProcedure, procedure=cls.instance_with_relation)
        cls.relations_queryset = cls.instance_with_relation.employees.all()
        cls.data = {
            'name': 'new procedure',
            'department': cls.instance.department.id
        }
        cls.update_data = {
            'name': 'updated procedure'
        }
        cls.invalid_data = {}


@pytest.mark.django_db
class TestProcedureViews(APITestCase,
                         BaseCRUDViewTest,
                         BaseDestroyWithUnarchivedRelationsViewTest,
                         BaseDestroyWithArchivedRelationsViewTest,
                         BaseUpdateWithoutRelationsViewTest,
                         BaseUpdateWithRelationsViewTest,
                         BaseUpdateDoNothingViewTest):
    model = Procedure
    serializer = ProcedureSerializer
    basename = 'procedure'

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.instance = mixer.blend(cls.model)
        cls.instance_data = {
            'name': cls.instance.name
        }
        cls.department = mixer.blend(Department)
        cls.data = {
            'name': 'test',
            'department': cls.department.id
        }
        cls.update_data = {
            'name': 'new test',
            'department': cls.department.id
        }
        cls.instance_with_relation = mixer.blend(cls.model)
        mixer.blend(MasterProcedure, procedure=cls.instance_with_relation)
        cls.relations_queryset = cls.instance_with_relation.employees.all()
