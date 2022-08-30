from core.services import BaseService

from .models import Material, Stock, ProductMaterial
from .serializers import MaterialSerializer, StockSerializer, ProductMaterialSerializer


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
