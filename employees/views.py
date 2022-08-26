from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from employees.services import MasterProcedureService, NewEmployeeService
from procedures.serializers import ProcedureSerializer

from .models import Employee, MasterProcedure
from .serializers import EmployeeSerializer, MasterProcedureListSerializer, MasterProcedureSerializer


class EmployeeViewSet(ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            id = NewEmployeeService(self.get_object()).destroy()
            return Response({'id': id}, status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status.HTTP_400_BAD_REQUEST)


class MasterProcedureViewSet(ModelViewSet):
    queryset = MasterProcedure.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return MasterProcedureListSerializer
        return MasterProcedureSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            id = MasterProcedureService(self.get_object()).destroy()
            return Response({'id': id}, status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status.HTTP_400_BAD_REQUEST)
