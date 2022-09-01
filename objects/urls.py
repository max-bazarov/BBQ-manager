from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import DepartemntListCreateView, ObjectViewSet

router = DefaultRouter()
router.register('objects', ObjectViewSet, 'object')

urlpatterns = [
    path('', include(router.urls)),
    path('objects/<int:object_id>/departments/', DepartemntListCreateView.as_view(), name='department'),
]
