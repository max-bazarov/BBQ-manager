from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from employees.services import NewEmployeeService

from .models import Employee
from .serializers import EmployeeSerializer


class EmployeeViewSet(ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            id = NewEmployeeService(self.get_object()).destroy()
            return Response({'id': id}, status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status.HTTP_400_BAD_REQUEST)
