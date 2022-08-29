import logging
from typing import Optional

import funcy
from django.core.exceptions import FieldDoesNotExist, ValidationError
from django.db.models import Model
from rest_framework.serializers import Serializer

log = logging.getLogger(__name__)


class BaseService:
    '''
    Base Service provides funcionality for basic operations with model instances.

    Usage: use this class as a mixin for other services.
    '''

    model: type[Model]
    serializer_class: Optional[type[Serializer]]
    related_name: str = None
    archivable_relation: bool = True

    def __init__(self, instance: Optional[Model] = None,
                 data: dict = None,
                 **kwargs) -> None:
        self.instance = instance
        self._kwargs = kwargs
        self.partial = self._kwargs.get('partial', False)
        self.data = data
        print(self.model.__name__, hasattr(self.model, 'archived'))

    def has_related(self) -> bool:
        if not self.related_name:
            return False
        return getattr(self.instance, self.related_name).exists()

    def is_all_related_archived(self) -> bool:
        if not self.related_name:
            return True
        return not getattr(self.instance, self.related_name).filter(archived=False).exists()

    def _validate_data(self) -> dict:
        serializer = self.serializer_class(data=self.data, partial=self.partial)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data

    def _get_instance_data(self, omit_id: bool = True) -> dict:
        '''Is needed for validation that we do not save the same data twice.'''

        data = {}
        for field in self.instance._meta.fields:
            data[field.name] = getattr(self.instance, field.name)
        if not omit_id:
            return data
        return funcy.omit(data, ['id'])

    def archive(self) -> Model:
        if not hasattr(self.instance, 'archived'):
            raise FieldDoesNotExist(f'{self.model.__name__} does not have field archived.')
        self.instance.archived = True
        self.instance.save()
        return self.instance

    def create(self) -> Model:
        return self.model.objects.create(**self._validate_data())

    def update(self) -> Model:
        is_changed = False
        data = self._get_instance_data()
        for k, v in self.data.items():
            if v != data[k]:
                is_changed = True
                break
        if not is_changed:
            return self.instance
        if self.has_related():
            new_instance_data = self._get_instance_data()
            new_instance_data.update(self.data)
            new_instance = self.__class__(data=new_instance_data).create()
            self.archive()
            return new_instance
        for k, v in self._validate_data().items():
            setattr(self.instance, k, v)
        self.instance.save()
        return self.instance

    def destroy(self) -> int:
        print('destroy', self.instance, hasattr(self.model, 'archived'))
        if self.has_related():
            if self.archivable_relation and self.is_all_related_archived():
                self.archive()
                return self.instance.id
            raise ValidationError(
                f'Instance of model {self.model.__name__} cannot be deleted '
                'as it has unarchived related objects.'
            )
        self.model.objects.get(id=self.instance.id).delete()
        return self.instance.id
