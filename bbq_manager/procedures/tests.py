import pytest
from django.test import TestCase
from django.urls import reverse
from mixer.backend.django import mixer
from rest_framework import status
from rest_framework.test import APITestCase

from core.tests import (BaseCreateTestMixin, BaseCRUDViewTest,
                        BaseDestroyTestMixin,
                        BaseDestroyWithArchivedRelationsTestMixin,
                        BaseDestroyWithArchivedRelationsViewTest,
                        BaseDestroyWithUnarchivedRelationsTestMixin,
                        BaseDestroyWithUnarchivedRelationsViewTest,
                        BaseSearchViewTest, BaseUpdateDoNothingViewTest,
                        BaseUpdateTestMixin,
                        BaseUpdateWithoutRelationsViewTest,
                        BaseUpdateWithRelationsViewTest)
from employees.models import MasterProcedure
from objects.models import Department

from .models import Procedure
from .serializers import ProcedureListSerializer, ProcedureSerializer
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
                         BaseUpdateDoNothingViewTest,
                         BaseSearchViewTest):
    model = Procedure
    serializer = ProcedureSerializer
    basename = 'procedure'
    serializers = {
        'list': ProcedureListSerializer
    }

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.base_url = reverse(f'{cls.basename}-list')
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
        cls.search_fields = [cls.instance.name, cls.instance.department.name]
        cls.instance_with_relation = mixer.blend(cls.model)
        mixer.blend(MasterProcedure, procedure=cls.instance_with_relation)
        cls.relations_queryset = cls.instance_with_relation.employees.all()

    def test_precedure_filter_by_obj_with_query_params(self):
        response = self.client.get(self.base_url, {'object': self.instance.department.object.id})

        assert response.status_code == status.HTTP_200_OK
        response_json = response.json()
        assert len(response_json) == self.model.objects.filter(
            department__object_id=self.instance.department.object.id
        ).count()
        assert response_json == self.serializers['list']([self.instance], many=True).data
