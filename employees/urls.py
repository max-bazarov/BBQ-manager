from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import EmployeeViewSet, MasterProcedureViewSet, EmployeeCreateListViewSet

router = DefaultRouter()

router.register('employees', EmployeeViewSet, 'employee')
router.register('master-procedures', MasterProcedureViewSet, 'master-procedure')

urlpatterns = [
    path('', include(router.urls)),
    path('object/<int:object_id>/emloyees/', EmployeeCreateListViewSet.as_view(), name='object-employee'),
    ]
