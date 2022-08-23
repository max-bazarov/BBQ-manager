from rest_framework.routers import DefaultRouter

from .views import UsedMaterialViewSet

router = DefaultRouter()

router.register('used-materials', UsedMaterialViewSet, basename='uses')

urlpatterns = router.urls
