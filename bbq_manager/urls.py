from django.contrib import admin
from django.urls import include, path
from django.conf import settings

from .yasg import urlpatterns as yasg_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include('procedures.urls'))
]

if settings.DEBUG:
    urlpatterns += yasg_urls

