from django.urls import path

from inventory.views import MaterialView

urlpatterns = [
    path('materials/', MaterialView.as_view({'get': 'list', 'post': 'create'})),
    path('materials/<int:pk>/', MaterialView.as_view({'get': 'retrieve', 'put': 'update'})),

]