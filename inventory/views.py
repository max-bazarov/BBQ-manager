from rest_framework import viewsets


from inventory.models import Material
from inventory.serializers import MaterialSerializer


class MaterialView(viewsets.ModelViewSet):
    """Создание материала и вывод всех материалов"""
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
