from core.services import BaseService

from .models import Material
from .serializers import MaterialSerializer


class MaterialService(BaseService):
    model = Material
    serializer_class = MaterialSerializer
    related_name = 'products'
