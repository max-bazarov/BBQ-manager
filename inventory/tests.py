import pytest
from django.test import TestCase
from django.urls import reverse
from mixer.backend.django import mixer
from rest_framework import status
from rest_framework.test import APITestCase

from core.tests import (BaseCRUDArchiveViewTest, NewBaseCreateTestMixin,
                        NewBaseDestroyTestMixin,
                        NewBaseDestroyWithUnarchivedRelationsTestMixin,
                        NewBaseUpdateTestMixin)

from purchases.models import UsedMaterial

from .models import Material, MaterialUnits
from .serializers import MaterialSerializer
from .services import MaterialService


class TestNewMaterialService(TestCase,
                             NewBaseCreateTestMixin,
                             NewBaseUpdateTestMixin,
                             NewBaseDestroyTestMixin,
                             NewBaseDestroyWithUnarchivedRelationsTestMixin):
    model = Material
    service = MaterialService

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.instance = mixer.blend(cls.model)
        cls.instance_with_relation = mixer.blend(cls.model)
        mixer.blend(UsedMaterial, material=cls.instance_with_relation)
        cls.relations_queryset = cls.instance_with_relation.uses.all()
        cls.data = {
            'name': 'some material',
            'unit': MaterialUnits.GRAMMS.value,
            'price': '1.00',
        }
        cls.invalid_data = {'price': 'test'}
        cls.update_data = {
            'name': 'Haircolor'
        }


@pytest.mark.django_db
class TestMaterialView(APITestCase, BaseCRUDArchiveViewTest):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.basename = 'material'
        cls.serializer = MaterialSerializer
        cls.model = Material
        cls.update_data = {
            'name': 'Hair Color 1',
            'price': '1.11',
            'unit': MaterialUnits.GRAMMS.value
        }

        cls.data = {
            'name': 'Hair Color',
            'price': 1.11,
            'unit': MaterialUnits.GRAMMS.value
        }
        cls.instance = mixer.blend(Material)
        cls.instance_with_relation = mixer.blend(Material)
        mixer.blend(UsedMaterial, material=cls.instance_with_relation)

    def test_destroy_view_with_relation(self):
        count = self.model.objects.count()
        url = reverse(self.basename + '-detail', args=[self.instance_with_relation.id])
        response = self.client.delete(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert count == self.model.objects.count()
