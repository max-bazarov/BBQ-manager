from rest_framework.viewsets import ModelViewSet

from .serializers import UsedMaterialSerializer
from .models import UsedMaterial


class UsedMaterialViewSet(ModelViewSet):
    serializer_class = UsedMaterialSerializer
    queryset = UsedMaterial.objects.all()
