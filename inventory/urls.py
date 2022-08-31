from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (MaterialCreateListViewSet, MaterialViewSet,
                    ProductMaterialViewSet, StockViewSet)

router = DefaultRouter()

router.register('materials', MaterialViewSet, 'material')
router.register('stocks', StockViewSet, 'stock')
router.register('product-materials', ProductMaterialViewSet, 'product-material')

urlpatterns = [
    path('', include(router.urls)),
    path(
        'object/<int:object_id>/materials/',
        MaterialCreateListViewSet.as_view(),
        name='object-material'
    )
]
