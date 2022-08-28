import pytest
from django.test import TestCase
from django.urls import reverse
from mixer.backend.django import mixer
from rest_framework import status
from rest_framework.test import APITestCase

from core.mixins.tests import BaseTestsUtilMixin
from core.tests import (BaseCRUDViewTest, NewBaseCreateTestMixin,
                        NewBaseDestroyTestMixin,
                        NewBaseDestroyWithArchivedRelationsTestMixin,
                        NewBaseDestroyWithUnarchivedRelationsTestMixin,
                        NewBaseUpdateTestMixin, BaseDestroyWithUnarchivedRelationsViewTest,
                        BaseDestroyWithArchivedRelationsViewTest)
from employees.models import MasterProcedure

from .models import Procedure
from .serializers import ProcedureSerializer
from .services import ProcedureNewService


@pytest.mark.django_db
class TestProcedureService(TestCase,
                           NewBaseCreateTestMixin,
                           NewBaseUpdateTestMixin,
                           NewBaseDestroyTestMixin,
                           NewBaseDestroyWithArchivedRelationsTestMixin,
                           NewBaseDestroyWithUnarchivedRelationsTestMixin):
    model = Procedure
    service = ProcedureNewService

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.instance = mixer.blend(cls.model)
        cls.instance_with_relation = mixer.blend(cls.model)
        mixer.blend(MasterProcedure, procedure=cls.instance_with_relation)
        cls.relations_queryset = cls.instance_with_relation.employees.all()
        cls.data = {
            'name': 'new procedure'
        }
        cls.update_data = {
            'name': 'updated procedure'
        }
        cls.invalid_data = {}


@pytest.mark.django_db
class TestProcedureViews(APITestCase,
                         BaseCRUDViewTest,
                         BaseDestroyWithUnarchivedRelationsViewTest,
                         BaseDestroyWithArchivedRelationsViewTest):
    model = Procedure
    serializer = ProcedureSerializer
    basename = 'procedure'

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.data = {
            'name': 'test'
        }
        cls.update_data = {
            'name': 'new test'
        }
        cls.instance = mixer.blend(cls.model)
        cls.instance_with_relation = mixer.blend(cls.model)
        mixer.blend(MasterProcedure, procedure=cls.instance_with_relation)
        cls.relations_queryset = cls.instance_with_relation.employees.all()

    def test_delete_without_relation(self):
        count = self.get_count()
        url = reverse('procedure-detail', args=[self.instance.id])
        response = self.client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert self.get_count() == count - 1
