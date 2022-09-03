from core.services import BaseService

from .models import Material, ProductMaterial, Stock
from .serializers import (MaterialSerializer, ProductMaterialSerializer,
                          StockSerializer)


class MaterialService(BaseService):
    model = Material
    serializer_class = MaterialSerializer
    related_name = 'products'


class StockService(BaseService):
    model = Stock
    serializer_class = StockSerializer


class ProductMaterialService(BaseService):
    model = ProductMaterial
    serializer_class = ProductMaterialSerializer
    related_name = 'materials'
