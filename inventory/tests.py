import pytest
from django.test import TestCase
from django.urls import reverse
from mixer.backend.django import mixer
from rest_framework import status
from rest_framework.test import APITestCase

from core.tests import (BaseCreateTestMixin,
                        BaseDestroyTestMixin, BaseDestroyWithArchivedRelationsViewTest,
                        BaseDestroyWithUnarchivedRelationsTestMixin, BaseDestroyWithUnarchivedRelationsViewTest, BaseListNestedViewTest,
                        BaseUpdateTestMixin, BaseCreateNestedViewTest)
from objects.models import Object
from purchases.models import UsedMaterial

from .models import Material, MaterialUnits
from .serializers import MaterialSerializer
from .services import MaterialService


class TestMaterialService(TestCase,
                          BaseCreateTestMixin,
                          BaseUpdateTestMixin,
                          BaseDestroyTestMixin,
                          BaseDestroyWithUnarchivedRelationsTestMixin):
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
            'object': cls.instance.object.id
        }
        cls.invalid_data = {'price': 'test'}
        cls.update_data = {
            'name': 'Haircolor'
        }


@pytest.mark.django_db
class TestMaterialView(APITestCase,
                       BaseCreateNestedViewTest,
                       BaseListNestedViewTest,
                       BaseDestroyWithUnarchivedRelationsViewTest):
    model = Material
    basename = 'material'
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.serializer = MaterialSerializer
        cls.object = mixer.blend(Object)
        cls.update_data = {
            'name': 'Hair Color 1',
            'price': '1.11',
            'unit': MaterialUnits.GRAMMS.value,
            'object': cls.object.id
        }
        cls.nested_url = reverse('object-material', args=[cls.object.id])
        cls.data = {
            'name': 'Hair Color',
            'price': 1.11,
            'unit': MaterialUnits.GRAMMS.value,
            'object': cls.object.id
        }
        cls.instance = mixer.blend(Material)
        cls.instance_with_relation = mixer.blend(Material)
        mixer.blend(UsedMaterial, material=cls.instance_with_relation)
        cls.nested_queryset = cls.object.materials.all()

    def test_destroy_view_with_relation(self):
        count = self.model.objects.count()
        url = reverse(self.basename + '-detail', args=[self.instance_with_relation.id])
        response = self.client.delete(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert count == self.model.objects.count()
