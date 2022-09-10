from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from procedures.filters import ProcedureFilter

from procedures.services import ProcedureService

from .models import Procedure
from .serializers import ProcedureSerializer


@swagger_auto_schema(manual_parameters=[openapi.Parameter('object', openapi.IN_QUERY, type=openapi.TYPE_INTEGER)])
class ProcedureViewSet(ModelViewSet):
    serializer_class = ProcedureSerializer
    queryset = Procedure.objects.all()
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'department__name']
    filterset_class = ProcedureFilter

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            updated_instance = ProcedureService(instance, data=request.data, **kwargs).update()
            return Response(ProcedureSerializer(updated_instance).data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            ProcedureService(instance=self.get_object()).destroy()
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)
