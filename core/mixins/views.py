from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from core.services import BaseService


class ArchiveViewMixin:
    '''
    This mixin provides `archive(self, request, *args, **kwargs)` method.
    It can only be used with models, which has archived field.
    '''
    service: type[BaseService]

    @action(detail=True, url_name='archive', methods=['put', 'patch'])
    def archive(self, request, *args, **kwargs):
        instance = self.get_object()
        archived_instance = self.service(instance, data=request.data, **kwargs).archive()
        return Response(self.serializer_class(archived_instance).data, status=status.HTTP_200_OK)
