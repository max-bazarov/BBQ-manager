from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from procedures.services import ProcedureService

from .models import Procedure
from .serializers import ProcedureSerializer


class ProcedureViewSet(ModelViewSet):
    serializer_class = ProcedureSerializer
    queryset = Procedure.objects.all()

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
