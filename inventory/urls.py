from rest_framework.routers import DefaultRouter

from .views import MaterialViewSet

router = DefaultRouter()

router.register('materials', MaterialViewSet, 'material')

urlpatterns = router.urls
