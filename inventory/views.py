from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from core.services import ArchiveService
from inventory.models import Material
from inventory.serializers import MaterialSerializer


class MaterialView(ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

    def update(self, request, *args, **kwargs):
        try:
            ArchiveService(self.get_object()).update(**request.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_201_CREATED)
