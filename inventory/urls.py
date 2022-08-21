from django.urls import path
from rest_framework.routers import DefaultRouter

from inventory.views import MaterialView

router = DefaultRouter()

router.register('materials', MaterialView, 'material')

urlpatterns = router.urls
