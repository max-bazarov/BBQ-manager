from itertools import permutations
from typing import Any

import funcy
from django.db.models import Model
from django.db.models.query import QuerySet
from django.urls import reverse
from rest_framework import status
from rest_framework.serializers import Serializer

from core.mixins.tests import BaseTestsUtilMixin
from core.services import BaseService


class BaseTest(BaseTestsUtilMixin):
    model: type[Model]
    service: type[BaseService]


class BaseCreateTestMixin(BaseTest):
    ''''''
    data: dict[str, Any]
    invalid_data: dict[str, Any]

    def test_create(self):
        count = self.get_count()
        self.service(data=self.data).create()

        assert self.get_count() == count + 1
        assert self.is_instance_exists(**self.data)

    def test_create_with_invalid_data(self):
        count = self.get_count()
        try:
            self.service(data=self.invalid_data).create()
        except Exception:
            pass
        else:
            assert False, f'{self.service.__name__} creates instances with invalid data.'
        assert self.get_count() == count


class BaseUpdateTestMixin(BaseTest):
    ''''''
    update_data: dict[str, Any]

    def test_partial_update(self):
        count = self.get_count()
        unchanged_data = funcy.omit(self.get_instance_data(), self.update_data)
        self.service(instance=self.instance, data=self.update_data, partial=True).update()
        instance = self.get_instance(id=self.instance.id)

        assert self.get_count() == count
        assert self.is_instance_exists(**self.update_data)
        for k, v in unchanged_data.items():
            assert v == getattr(instance, k)


class BaseDestroyTestMixin(BaseTest):

    def test_destroy(self):
        count = self.get_count()
        self.service(self.instance).destroy()

        assert self.get_count() == count - 1
        assert not self.is_instance_exists(id=self.instance.id)


class BaseDestroyWithUnarchivedRelationsTestMixin(BaseTest):
    instance_with_relation: Model
    relations_queryset: QuerySet

    def test_destroy_with_unarchived_relation(self):
        count = self.get_count()
        try:
            self.service(self.instance_with_relation).destroy()
        except Exception:
            pass
        else:
            assert False, 'Need to throw exception'

        assert self.get_count() == count
        assert not self.get_instance(self.instance_with_relation.id).archived


class BaseDestroyWithArchivedRelationsTestMixin(BaseTest):
    instance_with_relation: Model
    relations_queryset: QuerySet

    def test_destroy_with_archived_relation(self):
        self.relations_queryset.update(archived=True)
        count = self.get_count()
        self.service(self.instance_with_relation).destroy()

        assert self.get_count() == count
        assert self.get_instance(self.instance_with_relation.id).archived


class BaseViewTest(BaseTestsUtilMixin):
    '''
    Class for defining base attrs of Base View tests.
    '''
    model: type[Model]
    serializer: type[Serializer]
    instance: Model
    data: dict[str, str]
    basename: str
    serializers: dict[str, type[Serializer]] = dict()

    def check_update_data_same_fields_as_instance(self, instance):
        for k, v in self.update_data.items():
            value = getattr(instance, k)
            if isinstance(value, Model):
                value = value.id
            assert str(value) == str(v)


class BaseCreateViewTest(BaseViewTest):
    '''
    This class is ment to test CreateViews.

    Usage: Inherit from rest_framework.APITestCase and use this class as a mixin.
    Provide next attrs in setUpClass method:

    model: type[Model]
    serializer: type[Serializer]
    data: dict[str, Any]
    basename: str
    '''

    def test_create_view(self):
        count = self.model.objects.count()
        url = reverse(self.basename + '-list')
        response = self.client.post(url, self.data)

        assert response.status_code == status.HTTP_201_CREATED
        assert count + 1 == self.model.objects.count()
        assert response.json() == self.serializer(self.model.objects.last()).data
        assert self.model.objects.filter(**self.data).exists()
        assert all(
            v == self.data[k]
            for k, v in self.data.items()
        )


class BaseRetrieveViewTest(BaseViewTest):
    '''
    This class is ment to use retrive ednpoint.

    Usage: Inherit from rest_framework.APITestCase and use this class as a mixin.
    Provide next attrs in setUpClass method:

    model: type[Model]
    serializer: type[Serializer]
    instance: Model
    basename: str
    '''
    def test_retrieve_view(self):
        url = reverse(self.basename + '-detail', args=[self.instance.id])
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == self.serializer(self.instance).data


class BaseListViewTest(BaseViewTest):
    '''
    This class is ment to test listing endpoints.

    Usage: Inherit from rest_framework.APITestCase and use this class as a mixin.
    Provide next attrs in setUpClass method:

    model: type[Model]
    serializer: type[Serializer]
    instance: Model
    basename: str
    '''
    def test_list_view(self):
        serializer = self.serializers.get('list', self.serializer)
        url = reverse(self.basename + '-list')
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == serializer(self.model.objects.all(), many=True).data


class BaseUpdateViewTest(BaseViewTest):
    '''
    This class is ment to test Update endpoints.

    Usage: Inherit from rest_framework.APITestCase and use this class as a mixin.
    Provide next attrs in setUpClass method:

    model: type[Model]
    serializer: type[Serializer]
    instance: Model
    update_data: dict[str, Any]
    basename: str
    '''
    update_data: dict[str, Any]

    def test_update(self):
        count = self.model.objects.count()
        url = reverse(self.basename + '-detail', args=[self.instance.id])
        response = self.client.put(url, self.update_data, format='json')
        instance = self.model.objects.get(id=self.instance.pk)

        assert response.status_code == status.HTTP_200_OK, str(response.json())
        assert response.json() == self.serializer(instance).data
        assert count == self.model.objects.count()

        self.check_update_data_same_fields_as_instance(instance)

    def test_partial_update(self):
        count = self.model.objects.count()
        url = reverse(self.basename + '-detail', args=[self.instance.id])
        response = self.client.patch(url, self.update_data, format='json')
        instance = self.model.objects.get(id=self.instance.pk)

        assert response.status_code == status.HTTP_200_OK, response.json()
        assert response.json() == self.serializer(instance).data
        assert count == self.model.objects.count()

        self.check_update_data_same_fields_as_instance(instance)


class BaseDestroyViewTest(BaseViewTest):
    '''
    This class is ment to test destroy endpoints.

    Usage: Inherit from rest_framework.APITestCase and use this class as a mixin.
    Provide next attrs in setUpClass method:

    model: type[Model]
    instance: Model
    basename: str
    '''

    def test_destroy_view(self):
        count = self.model.objects.count()
        url = reverse(self.basename + '-detail', args=[self.instance.id])
        response = self.client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert count - 1 == self.model.objects.count()


class BaseCRUDViewTest(BaseCreateViewTest,
                       BaseRetrieveViewTest,
                       BaseListViewTest,
                       BaseUpdateViewTest,
                       BaseDestroyViewTest):
    '''
    This test is a combination of all base crud tests.

    Usage: Inherit from rest_framework.APITestCase and use this class as a mixin.
    Provide next attrs in setUpClass method:

    model: type[Model]
    serializer: type[Serializer]
    instance: Model
    data: dict[str, Any]
    update_data: dict[str, Any]
    basename: str
    '''
    pass


class BaseArchiveViewTest(BaseViewTest):
    '''
    Usage: Inherit from rest_framework.APITestCase and use this class as a mixin.
    Provide next attrs in setUpClass method:

    model: type[Model]
    serializer: type[Serializer]
    instance: Model
    update_data: dict[str, Any]
    basename: str
    '''
    update_data: dict[str, Any]

    def test_update(self):
        count = self.model.objects.count()
        url = reverse(self.basename + '-detail', args=[self.instance.id])
        response = self.client.put(url, self.update_data, format='json')

        assert response.status_code == status.HTTP_200_OK, str(response.data())
        assert count + 1 == self.model.objects.count()
        assert self.model.objects.filter(id=self.instance.id).exists()
        assert self.model.objects.get(id=self.instance.id).archived
        new_instance = self.model.objects.last()
        assert not new_instance.archived
        assert response.json() == self.serializer(new_instance).data

    def test_partial_update(self):
        count = self.model.objects.count()
        url = reverse(self.basename + '-detail', args=[self.instance.id])
        response = self.client.patch(url, self.update_data, format='json')

        assert response.status_code == status.HTTP_200_OK, str(response.json())
        assert count + 1 == self.model.objects.count()
        assert self.model.objects.filter(id=self.instance.id).exists()
        assert self.model.objects.get(id=self.instance.id).archived
        assert response.json() == self.serializer(self.model.objects.last()).data

    def test_archive(self):
        url = reverse(self.basename + '-archive', args=[self.instance.id])
        response = self.client.put(url)

        assert response.status_code == status.HTTP_200_OK
        assert self.get_instance(self.instance.id).archived


class BaseCRUDArchiveViewTest(BaseCreateViewTest,
                              BaseRetrieveViewTest,
                              BaseListViewTest,
                              BaseArchiveViewTest,
                              BaseDestroyViewTest):
    '''
    This test is a combination of all base crd and archive tests.

    Usage: Inherit from rest_framework.APITestCase and use this class as a mixin.
    Provide next attrs in setUpClass method:

    model: type[Model] # Model class of
    serializer: type[Serializer]
    instance: Model
    data: dict[str, Any]
    update_data: dict[str, Any]
    basename: str
    '''
    pass


class DestroyInstancesWithRelationalDependenciesTestMixin(BaseTestsUtilMixin):
    '''
    This class is ment to test services which work with instances that are not permitted
    to delete instanced, which have related objects.
    '''
    instance: Model
    model: type[Model]
    instance_with_relation: Model
    destroy_service: type  # service class

    def test_delete_without_relations(self):
        count = self.get_count()
        self.destroy_service(self.instance).destroy()

        assert self.get_count() == count - 1, (
            f'{self.destroy_service.__name__} does not destroy '
            'instance without relations.'
        )
        assert not self.model.objects.filter(id=self.instance.id).exists(), (
            f'{self.destroy_service.__name__} destroys '
            'wrong instance'
        )

    def test_delete_with_relations(self):
        count = self.get_count()

        try:
            self.destroy_service(self.instance_with_relation).destroy()
        except Exception:
            pass
        else:
            assert False, (
                f'{self.destroy_service.__name__} does not raises when trying '
                'to delete instance with relations'
            )
        assert count == self.get_count(), (
            f'{self.destroy_service.__name__} destroys instance with existing relations.'
        )


class BaseCreateNestedViewTest(BaseTestsUtilMixin):
    nested_url: str

    def test_create_view(self):
        count = self.get_count()
        response = self.client.post(self.nested_url, self.data)

        assert response.status_code == status.HTTP_201_CREATED, response.json()
        assert self.get_count() == count + 1


class BaseListNestedViewTest(BaseTestsUtilMixin):
    nested_url: str
    nested_queryset: QuerySet

    def test_list(self):
        response = self.client.get(self.nested_url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == self.nested_queryset.count()


class BaseDestroyWithUnarchivedRelationsViewTest(BaseViewTest):
    instance_with_relation: Model

    def test_delete_with_unarchived_relation_view(self):
        count = self.get_count()
        url = reverse(self.basename + '-detail', args=[self.instance_with_relation.id])
        response = self.client.delete(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.get_count() == count
        assert not self.get_instance(self.instance_with_relation.id).archived


class BaseDestroyWithArchivedRelationsViewTest(BaseViewTest):
    instance_with_relation: Model
    relations_queryset: QuerySet

    def test_delete_with_archived_relation_view(self):
        self.relations_queryset.update(archived=True)
        count = self.get_count()
        url = reverse(self.basename + '-detail', args=[self.instance_with_relation.id])
        response = self.client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT, response.json()
        assert self.get_count() == count
        assert self.get_instance(self.instance_with_relation.id).archived


class BaseUpdateWithRelationsViewTest(BaseViewTest):
    instance_with_relation: Model

    def test_update_with_relation_view(self):
        count = self.get_count()
        url = reverse(self.basename + '-detail', args=[self.instance_with_relation.id])
        response = self.client.put(url, self.update_data, format='json')

        assert response.status_code == status.HTTP_200_OK, str(response.data())
        assert count + 1 == self.get_count()
        assert self.model.objects.filter(id=self.instance_with_relation.id).exists()
        assert self.model.objects.get(id=self.instance_with_relation.id).archived
        new_instance = self.model.objects.last()
        assert not new_instance.archived
        assert response.json() == self.serializer(new_instance).data
        self.check_update_data_same_fields_as_instance(new_instance)

    def test_partial_update_with_relation_view(self):
        count = self.get_count()
        url = reverse(self.basename + '-detail', args=[self.instance_with_relation.id])
        response = self.client.put(url, self.update_data, format='json')

        assert response.status_code == status.HTTP_200_OK, str(response.data())
        assert count + 1 == self.get_count()
        assert self.model.objects.filter(id=self.instance_with_relation.id).exists()
        assert self.model.objects.get(id=self.instance_with_relation.id).archived
        new_instance = self.model.objects.last()
        assert not new_instance.archived
        assert response.json() == self.serializer(new_instance).data
        self.check_update_data_same_fields_as_instance(new_instance)


class BaseUpdateWithoutRelationsViewTest(BaseViewTest):
    instance_with_relation: Model

    def test_update_without_relation_view(self):
        count = self.get_count()
        url = reverse(self.basename + '-detail', args=[self.instance.id])
        response = self.client.put(url, self.update_data, format='json')
        instance = self.model.objects.get(id=self.instance.pk)

        assert response.status_code == status.HTTP_200_OK, str(response.data())
        assert count == self.get_count()
        assert self.model.objects.filter(id=self.instance.id).exists()
        self.check_update_data_same_fields_as_instance(instance)

    def test_partial_update_without_relation_view(self):
        count = self.get_count()
        url = reverse(self.basename + '-detail', args=[self.instance.id])
        response = self.client.patch(url, self.update_data, format='json')
        instance = self.model.objects.get(id=self.instance.pk)

        assert response.status_code == status.HTTP_200_OK, str(response.data())
        assert count == self.get_count()
        assert self.model.objects.filter(id=self.instance.id).exists()
        self.check_update_data_same_fields_as_instance(instance)


class BaseUpdateDoNothingViewTest(BaseViewTest):

    instance_data: dict[str, Any]

    def test_update_do_nothing(self):
        count = self.get_count()
        url = reverse(self.basename + '-detail', args=[self.instance.id])
        response = self.client.put(url, self.instance_data, format='json')

        assert response.status_code == status.HTTP_200_OK, str(response.data())
        assert count == self.get_count()
        assert self.model.objects.filter(id=self.instance.id).exists()
        assert not self.get_instance(self.instance.id).archived

    def test_partial_update_do_nothing(self):
        count = self.get_count()
        url = reverse(self.basename + '-detail', args=[self.instance.id])
        response = self.client.patch(url, self.instance_data, format='json')

        assert response.status_code == status.HTTP_200_OK, str(response.data())
        assert count == self.get_count()
        assert self.model.objects.filter(id=self.instance.id).exists()
        assert not self.get_instance(self.instance.id).archived


class BaseSearchViewTest(BaseViewTest):
    search_fields: list[str]

    def test_search(self):
        search_fields = permutations(self.search_fields, len(self.search_fields))
        for fields in search_fields:
            url = reverse(self.basename + '-list') + '?search=' + '+'.join(fields)
            response = self.client.get(url)

            assert response.status_code == status.HTTP_200_OK
            assert response.json()[0] == self.serializer(self.instance).data