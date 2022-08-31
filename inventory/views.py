from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from inventory.models import Material, ProductMaterial, Stock
from inventory.serializers import (MaterialSerializer,
                                   ProductMaterialSerializer, StockSerializer)

from .services import MaterialService, ProductMaterialService


class MaterialCreateListViewSet(ListCreateAPIView):
    serializer_class = MaterialSerializer
    swagger_tags = ['materials']

    def get_queryset(self):
        obj_id = self.kwargs['object_id']
        return Material.objects.filter(object=obj_id)

    def perform_create(self, serializer):
        serializer.save(object_id=self.kwargs['object_id'])


class MaterialViewSet(ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            updated_instance = MaterialService(instance, data=request.data, **kwargs).update()
            return Response(MaterialSerializer(updated_instance).data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            MaterialService(instance=self.get_object()).destroy()
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)


class StockViewSet(ModelViewSet):
    serializer_class = StockSerializer
    queryset = Stock.objects.all()


class ProductMaterialViewSet(ModelViewSet):
    queryset = ProductMaterial.objects.all()
    serializer_class = ProductMaterialSerializer

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            updated_instance = ProductMaterialService(instance,
                                                      data=request.data, **kwargs).update()
            return Response(ProductMaterialSerializer(updated_instance).data,
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            ProductMaterialService(instance=self.get_object()).destroy()
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)
