from django.urls import path
from drf_yasg import openapi
from drf_yasg.inspectors import SwaggerAutoSchema
from drf_yasg.views import get_schema_view
from rest_framework import permissions


class CustomAutoSchema(SwaggerAutoSchema):

    def get_tags(self, operation_keys=None):
        tags = self.overrides.get('tags', None) or getattr(self.view, 'swagger_tags', [])
        if not tags:
            tags = [operation_keys[0]]

        return tags


schema_view = get_schema_view(
    openapi.Info(
        title="BBQ API",
        default_version='v1',
        description="Description",
        terms_of_service="",
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
