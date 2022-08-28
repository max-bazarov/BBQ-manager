from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import MaterialCreateListViewSet, MaterialViewSet

router = DefaultRouter()

router.register('materials', MaterialViewSet, 'material')

urlpatterns = [
    path('', include(router.urls)),
    path('object/<int:object_id>/materials/', MaterialCreateListViewSet.as_view())
]
