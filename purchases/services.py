from core.services import BaseService

from .models import UsedMaterial
from .serializers import UsedMaterialSerializer


class UsedMaterialService(BaseService):
    model = UsedMaterial
    serializer_class = UsedMaterialSerializer
