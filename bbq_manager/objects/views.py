from rest_framework.generics import ListCreateAPIView
from rest_framework.viewsets import ModelViewSet

from .models import Department, Object
from .serializers import DepartmentSerializer, ObjectSerializer


class ObjectViewSet(ModelViewSet):
    serializer_class = ObjectSerializer
    queryset = Object.objects.all()


class DepartemntListCreateView(ListCreateAPIView):
    serializer_class = DepartmentSerializer

    def get_queryset(self):
        return Department.objects.filter(object_id=self.kwargs['object_id'])
