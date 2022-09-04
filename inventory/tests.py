import pytest
from django.test import TestCase
from django.urls import reverse
from mixer.backend.django import mixer
from rest_framework import status
from rest_framework.test import APITestCase

from core.tests import (BaseCreateNestedViewTest, BaseCreateTestMixin,
                        BaseCRUDViewTest, BaseDestroyTestMixin,
                        BaseDestroyWithUnarchivedRelationsTestMixin,
                        BaseDestroyWithUnarchivedRelationsViewTest,
                        BaseListNestedViewTest, BaseUpdateDoNothingViewTest,
                        BaseUpdateTestMixin,
                        BaseUpdateWithoutRelationsViewTest,
                        BaseUpdateWithRelationsViewTest,
                        BaseSearchViewTest)
from objects.models import Object
from purchases.models import UsedMaterial, PurchaseProcedure

from .models import Material, MaterialUnits, ProductMaterial, Stock
from .serializers import (MaterialSerializer, ProductMaterialSerializer,
                          StockSerializer)
from .services import MaterialService, ProductMaterialService, StockService


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
        mixer.blend(ProductMaterial, material=cls.instance_with_relation)
        cls.relations_queryset = cls.instance_with_relation.products.all()
        cls.data = {
            'name': 'some material',
            'unit': MaterialUnits.GRAMMS.value,
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
                       BaseUpdateWithoutRelationsViewTest,
                       BaseUpdateWithRelationsViewTest,
                       BaseUpdateDoNothingViewTest,
                       BaseSearchViewTest):
    model = Material
    basename = 'material'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.serializer = MaterialSerializer
        cls.object = mixer.blend(Object)

        cls.update_data = {
            'name': 'Hair Color 1',
            'unit': MaterialUnits.GRAMMS.value,
            'object': cls.object.id
        }
        cls.nested_url = reverse('object-material', args=[cls.object.id])
        cls.data = {
            'name': 'Hair Color',
            'unit': MaterialUnits.GRAMMS.value,
            'object': cls.object.id
        }
        cls.instance = mixer.blend(Material)
        cls.instance_data = {
            'name': cls.instance.name
        }
        cls.instance_with_relation = mixer.blend(Material)
        mixer.blend(ProductMaterial, material=cls.instance_with_relation)
        cls.nested_queryset = cls.object.materials.all()
        cls.search_fields = ['name']

    def test_destroy_view_with_relation(self):
        count = self.model.objects.count()
        url = reverse(self.basename + '-detail', args=[self.instance_with_relation.id])
        response = self.client.delete(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert count == self.model.objects.count()


class TestStockService(TestCase,
                       BaseCreateTestMixin,
                       BaseDestroyTestMixin,
                       BaseUpdateTestMixin):
    model = Stock
    service = StockService

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.instance = mixer.blend(cls.model)
        cls.data = {
            'price': '1.23',
            'material': mixer.blend(Material).id
        }
        cls.update_data = {
            'price': '2.28',
            'material': mixer.blend(Material).id
        }
        cls.invalid_data = {
            'material': 'hahahahha funny'
        }


@pytest.mark.django_db
class TestStockView(APITestCase,
                    BaseCRUDViewTest,
                    BaseCreateNestedViewTest,
                    BaseListNestedViewTest):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.object = mixer.blend(Object)
        cls.nested_url = reverse('object-stock', args=[cls.object.id])
        cls.serializer = StockSerializer
        cls.model = Stock
        cls.basename = 'stock'
        cls.data = {
            'price': '1.23',
            'material': mixer.blend(Material).id
        }
        cls.update_data = {
            'price': '2.28',
            'material': mixer.blend(Material).id
        }
        cls.instance = mixer.blend(Stock)
        cls.nested_queryset = cls.object.materials.all()
        cls.url_for_stock_remains = reverse('object-stock-remain', args=[cls.object.id])

    @staticmethod
    def check_amount(expected_amount, response: list[dict]):
        for item in response:
            id, amount = item['id'], item['amount']
            assert expected_amount[id] == amount

    def test_stock_remains_with_anything_view(self):
        """This test for situation when we dont have materials in stock and UsedMaterials"""
        material = mixer.blend(Material, object=self.object)
        response = self.client.get(self.url_for_stock_remains)
        expected_amount = {
            material.id: 0
        }

        assert response.status_code == status.HTTP_200_OK
        response_json = response.json()
        assert len(response_json) == self.nested_queryset.count()
        self.check_amount(expected_amount, response_json)

    def test_stock_remains_with_stock_view(self):
        """This test for situation when we have materials in stock"""
        material = mixer.blend(Material, object=self.object)
        mixer.blend(Stock, material=material, amount=100)
        response = self.client.get(self.url_for_stock_remains)
        expected_amount = {
            material.id: 100
        }

        assert response.status_code == status.HTTP_200_OK
        response_json = response.json()
        assert len(response_json) == self.nested_queryset.count()
        self.check_amount(expected_amount, response_json)

    def test_stock_remains_with_stock_view(self):
        """This test for clasic situation"""
        material = mixer.blend(Material, object=self.object)
        mixer.blend(Stock, material=material, amount=100)
        mixer.blend(UsedMaterial, material=mixer.blend(ProductMaterial,
                                                       material=material), amount=10)
        response = self.client.get(self.url_for_stock_remains)
        expected_amount = {
            material.id: 90
        }

        assert response.status_code == status.HTTP_200_OK
        response_json = response.json()
        assert len(response_json) == self.nested_queryset.count()
        self.check_amount(expected_amount, response_json)

    def test_stock_remains_with_multiple_stock_view(self):
        """This test for situation when we have multiple stock materials of the same Material id """
        material = mixer.blend(Material, object=self.object)
        mixer.blend(Stock, material=material, amount=10)
        mixer.blend(Stock, material=material, amount=30)
        response = self.client.get(self.url_for_stock_remains)
        expected_amount = {
            material.id: 40
        }

        assert response.status_code == status.HTTP_200_OK
        response_json = response.json()
        assert len(response_json) == self.nested_queryset.count()
        self.check_amount(expected_amount, response_json)

    def test_stock_remains_with_another_material_view(self):
        """This test for situation when we have another material in UsedMaterials"""
        material = mixer.blend(Material, object=self.object)
        mixer.blend(Stock, material=material, amount=10)
        mixer.blend(UsedMaterial, material=mixer.blend(ProductMaterial,
                                                       material=mixer.blend(Material)), amount=30)
        response = self.client.get(self.url_for_stock_remains)
        expected_amount = {
            material.id: 10
        }

        assert response.status_code == status.HTTP_200_OK
        response_json = response.json()
        assert len(response_json) == self.nested_queryset.count()
        self.check_amount(expected_amount, response_json)

    def test_stock_remains_with_multiple_used_material_view(self):
        """This test for situation when we have multiple material
        in UsedMaterials of the same Material id"""
        material = mixer.blend(Material, object=self.object)
        mixer.blend(Stock, material=material, amount=100)
        mixer.blend(UsedMaterial, material=mixer.blend(ProductMaterial,
                                                       material=material), amount=10)
        mixer.blend(UsedMaterial, material=mixer.blend(ProductMaterial,
                                                       material=material), amount=30)
        response = self.client.get(self.url_for_stock_remains)
        expected_amount = {
            material.id: 60
        }

        assert response.status_code == status.HTTP_200_OK
        response_json = response.json()
        assert len(response_json) == self.nested_queryset.count()
        self.check_amount(expected_amount, response_json)

    def test_stock_remains_with_multiple_used_material_for_the_same_procedure_view(self):
        material = mixer.blend(Material, object=self.object)
        mixer.blend(Stock, material=material, amount=100)
        product_material = mixer.blend(ProductMaterial, material=material)
        purchase_procedure = mixer.blend(PurchaseProcedure)
        mixer.blend(UsedMaterial, amount=1, pourchase=purchase_procedure, material=product_material)
        mixer.blend(UsedMaterial, amount=1, pourchase=purchase_procedure, material=product_material)
        response = self.client.get(self.url_for_stock_remains)
        expected_amount = {
            material.id: 98
        }

        assert response.status_code == status.HTTP_200_OK
        response_json = response.json()
        assert len(response_json) == self.nested_queryset.count()
        self.check_amount(expected_amount, response_json)


class TestProductMaterialService(TestCase,
                                 BaseCreateTestMixin,
                                 BaseUpdateTestMixin,
                                 BaseDestroyTestMixin,
                                 BaseDestroyWithUnarchivedRelationsTestMixin,):

    model = ProductMaterial
    service = ProductMaterialService

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.instance = mixer.blend(cls.model)
        cls.instance_with_relation = mixer.blend(cls.model)
        mixer.blend(UsedMaterial, material=cls.instance_with_relation)
        cls.relations_queryset = cls.instance_with_relation.materials.all()
        cls.data = {
            'material': mixer.blend(Material).id,
            'price': '1.23'
        }
        cls.invalid_data = {'material': 'test'}
        cls.update_data = {
            'price': '2.28'
        }


@pytest.mark.django_db
class TestProductMaterialView(APITestCase,
                              BaseCRUDViewTest,
                              BaseCreateNestedViewTest,
                              BaseListNestedViewTest,
                              BaseDestroyWithUnarchivedRelationsViewTest,
                              BaseUpdateWithoutRelationsViewTest,
                              BaseUpdateWithRelationsViewTest,
                              BaseUpdateDoNothingViewTest,
                              ):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.model = ProductMaterial
        cls.serializer = ProductMaterialSerializer
        cls.basename = 'product-material'
        cls.object = mixer.blend(Object)
        cls.nested_url = reverse('object-product-material', args=[cls.object.id])
        cls.instance = mixer.blend(cls.model)
        cls.instance_data = {
            'archived': cls.instance.archived
        }
        cls.data = {
            'material': mixer.blend(Material).id,
            'price': '1.23'
        }
        cls.update_data = {
            'material': mixer.blend(Material).id,
            'price': '1.23'
        }
        cls.instance_with_relation = mixer.blend(cls.model)
        mixer.blend(UsedMaterial, material=cls.instance_with_relation)
        cls.nested_queryset = cls.object.materials.all()
