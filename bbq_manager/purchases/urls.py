from rest_framework.routers import DefaultRouter

from .views import UsedMaterialViewSet

router = DefaultRouter()

router.register('used-materials', UsedMaterialViewSet, basename='used-material')

urlpatterns = router.urls
