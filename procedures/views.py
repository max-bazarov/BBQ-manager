from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.exceptions import APIException

from procedures.services import ProcedureService

from .models import Procedure
from .serializers import ProcedureSerializer


class ProcedureViewSet(ModelViewSet):
    serializer_class = ProcedureSerializer
    queryset = Procedure.objects.all()

    def destroy(self, request, *args, **kwargs):
        try:
            ProcedureService(self.get_object()).destroy()
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)