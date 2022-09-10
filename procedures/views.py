from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from procedures.filters import ProcedureFilter

from procedures.services import ProcedureService

from .models import Procedure
from .serializers import ProcedureListSerializer, ProcedureSerializer


class ProcedureViewSet(ModelViewSet):
    serializer_class = ProcedureSerializer
    queryset = Procedure.objects.all()
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'department__name']
    filterset_class = ProcedureFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return ProcedureListSerializer
        return ProcedureSerializer

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
