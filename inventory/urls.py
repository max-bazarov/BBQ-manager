from django.urls import path

from inventory.views import MaterialView

urlpatterns = [
    path('', MaterialView.as_view({'get': 'list', 'post': 'create'})),

]