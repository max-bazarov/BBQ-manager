from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from employees.filters import MasterProcedureFilter
from employees.services import EmployeeService, MasterProcedureService

from .models import Employee, MasterProcedure
from .serializers import (EmployeeSerializer, MasterProcedureListSerializer,
                          MasterProcedureSerializer)


class EmployeeCreateListViewSet(ListCreateAPIView):
    serializer_class = EmployeeSerializer
    swagger_tags = ['employees']

    def get_queryset(self):
        obj_id = self.kwargs['object_id']
        return Employee.objects.filter(object=obj_id)


class EmployeeViewSet(ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            updated_instance = EmployeeService(instance, data=request.data, **kwargs).update()
            return Response(EmployeeSerializer(updated_instance).data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            EmployeeService(self.get_object()).destroy()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status.HTTP_400_BAD_REQUEST)


class MasterProcedureViewSet(ModelViewSet):
    queryset = MasterProcedure.objects.all()
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_class = MasterProcedureFilter
    search_fields = ['procedure__name', 'employee__first_name', 'employee__last_name']

    def get_serializer_class(self):
        if self.action == 'list':
            return MasterProcedureListSerializer
        return MasterProcedureSerializer

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            updated_instance = MasterProcedureService(instance,
                                                      data=request.data, **kwargs).update()
            return Response(MasterProcedureSerializer(updated_instance).data,
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            MasterProcedureService(self.get_object()).destroy()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status.HTTP_400_BAD_REQUEST)
