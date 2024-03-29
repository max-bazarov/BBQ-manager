from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (EmployeeCreateListViewSet, EmployeeViewSet,
                    MasterProcedureViewSet)

router = DefaultRouter()

router.register('employees', EmployeeViewSet, 'employee')
router.register('master-procedures', MasterProcedureViewSet, 'master-procedure')

urlpatterns = [
    path('', include(router.urls)),
    path(
        'objects/<int:object_id>/employees/',
        EmployeeCreateListViewSet.as_view(),
        name='object-employee'
    ),
]
