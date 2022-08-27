from rest_framework.routers import DefaultRouter

from .views import EmployeeViewSet, MasterProcedureViewSet

router = DefaultRouter()

router.register('employees', EmployeeViewSet, 'employee')
router.register('master-procedures', MasterProcedureViewSet, 'master-procedure')

urlpatterns = router.urls
