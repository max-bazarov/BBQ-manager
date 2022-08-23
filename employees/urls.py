from rest_framework.routers import DefaultRouter

from .views import EmployeeViewSet

router = DefaultRouter()

router.register('employees', EmployeeViewSet, 'employee')

urlpatterns = router.urls
