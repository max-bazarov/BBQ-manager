import pytest

from django.test import TestCase

from .models import Material, MaterialUnits
from .services import MaterialServiceCreate


class TestMaterialCreateService(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.material_data = {
            'name': 'Hair Color',
            'price': 1.11,
            'unit': MaterialUnits.GRAMMS.value
        }

    @pytest.mark.django_db
    def test_material_create_service_create_instance(self):
        materials_count = Material.objects.count()

        material = MaterialServiceCreate.execute(inputs=self.material_data)

        assert Material.objects.count() == materials_count + 1, (
            f'{MaterialServiceCreate.__name__} does not create instance'
        )
        assert isinstance(material, Material), (
            f'{MaterialServiceCreate.__name__} does not return instance. Got: {material.__class__.__name__}'    
        )

