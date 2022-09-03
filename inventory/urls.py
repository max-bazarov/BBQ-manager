from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (MaterialCreateListViewSet, MaterialViewSet,
                    ProductMaterialViewSet,
                    StockViewSet,
                    StockCreateListViewSet,
                    StockRemainGetView,
                    ProductMaterialCreateListViewSet)

router = DefaultRouter()

router.register('materials', MaterialViewSet, 'material')
router.register('stocks', StockViewSet, 'stock')
router.register('product-materials', ProductMaterialViewSet, 'product-material')


class ProducMaterialCreateListViewSet:
    pass


urlpatterns = [
    path('', include(router.urls)),
    path(
        'objects/<int:object_id>/materials/',
        MaterialCreateListViewSet.as_view(),
        name='object-material'
    ),
    path('objects/<int:object_id>/stock/',
         StockCreateListViewSet.as_view(),
         name='object-stock'
         ),
    path('objects/<int:object_id>/stock/remain/',
         StockRemainGetView.as_view(),
         name='object-stock-remain'),
    path('objects/<int:object_id>/product-material/',
         ProductMaterialCreateListViewSet.as_view(),
         name='object-product-material'),
]
