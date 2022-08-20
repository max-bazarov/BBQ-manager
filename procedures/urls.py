from xml.etree.ElementInclude import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ProcedureViewSet

router = DefaultRouter()

router.register('procedures', ProcedureViewSet, 'procedure')

urlpatterns = router.urls
