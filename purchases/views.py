from rest_framework.viewsets import ModelViewSet

from .models import UsedMaterial
from .serializers import UsedMaterialSerializer


class UsedMaterialViewSet(ModelViewSet):
    serializer_class = UsedMaterialSerializer
    queryset = UsedMaterial.objects.all()
