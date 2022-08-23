from typing import Any

from django.db.models import Model
from django.urls import reverse
from rest_framework import status
from rest_framework.serializers import Serializer
from service_objects.services import Service


class BaseTestsUtilMixin:
    model: type[Model]

    def get_count(self) -> int:
        return self.model.objects.count()


class BaseCreateServiceTest:
    '''
    Base Create Service Test is ment to test service classes, which are responsible for
    creation operations. In order to use it you should inherit from django.test.TestCase
    and use this class as a mixin.

    Usage: inherit from django.test.TestCase and use this class as mixin.

    Note: Works with services, which are inherited from service_objects.services.Service only.
    '''

    model: type[Model]
    data: dict[str, Any]
    create_service: type[Service]

    def test_create(self):
        count = self.model.objects.count()
        instance = self.create_service.execute(self.data)

        assert count + 1 == self.model.objects.count(), (
            f'{self.create_service.__class__.__name__} does not create instance'
        )
        assert isinstance(instance, self.model), (
            f'{self.create_service.__class__.__name__} create method does not return instance'
        )
        print(instance.id, instance)
        for k, v in self.data.items():
            assert v == getattr(instance, k)


class BaseDestroyServiceTest:
    '''
    Base Destroy Service Test is ment to test service classes, wher are responsible for
    destroy operations.

    Usage: inherit from django.test.TestCase and use this class as mixin.

    Note: Works with services, which are inherited from service_objects.services.Service only.

    '''

    instance: Model
    create_service: type[Service]

    def test_destroy(self):
        count = self.model.objects.count()
        instance = self.model.objects.first()

        self.destroy_service.execute({'id': instance.id})
        assert count - 1 == self.model.objects.count(), ('fail')


class BaseArchiveServiceTest:
    '''
    This class is ment to test archive services.

    Usage: inherit from django.test.TestCase and use this class as mixin.

    Note: Works with services, which are inherited from service_objects.services.Service only.
    '''

    def test_archive(self):
        count = self.model.objects.count()
        archived_id = self.archive_service(self.instance).archive()

        assert count == self.model.objects.count(), (
            f'{self.archive_service.__class__.__name__} does not archive instance'
        )
        assert archived_id == self.instance.pk, (
            f'{self.archive_service.__class__.__name__} archive method does not return instance id'
        )

    def test_update(self):
        count = self.model.objects.count()
        new_instance = self.archive_service(self.instance).update(**self.update_data)
        unchanged_fields = [
            f.name for f in self.instance._meta.fields
            if f.name not in self.update_data and f.name != 'id'
        ]

        are_same = all(
            getattr(self.instance, f) == getattr(new_instance, f) for f in unchanged_fields
        )
        assert are_same, (
            f'{self.archive_service.__class__.__name__} new instance data'
            f' is not equal to old instance data'
        )
        assert count + 1 == self.model.objects.count(), (
            f'{self.archive_service.__class__.__name__} does not create updated instance'
        )
        assert isinstance(new_instance, self.model), (
            f'{self.archive_service.__class__.__name__} update method does not return new instance'
        )
        assert self.model.objects.first().archived is True, (
            f'{self.archive_service.__class__.__name__} update method does not archive instance'
        )
        assert self.update_data['price'] == new_instance.price, (
            f'{self.archive_service.__class__.__name__} update method does not update instance'
        )


class BaseViewTest:
    '''
    Class for defining base attrs of Base View tests.
    '''
    model: type[Model]
    serializer: type[Serializer]
    instance: Model
    data: dict[str, str]
    basename: str


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
        url = reverse(self.basename + '-list')
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == self.serializer(self.model.objects.all(), many=True).data


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

    def test_update_view(self):
        count = self.model.objects.count()
        url = reverse(self.basename + '-detail', args=[self.instance.id])
        response = self.client.put(url, self.update_data)
        instance = self.model.objects.get(id=self.instance.pk)

        assert response.status_code == status.HTTP_200_OK, str(response.json())
        assert response.json() == self.serializer(instance).data
        assert count == self.model.objects.count()
        assert all(
            v == getattr(instance, k)
            for k, v in self.update_data.items()
        )

    def test_partial_update_view(self):
        count = self.model.objects.count()
        url = reverse(self.basename + '-detail', args=[self.instance.id])
        response = self.client.patch(url, self.update_data)
        instance = self.model.objects.get(id=self.instance.pk)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == self.serializer(instance).data
        assert count == self.model.objects.count()
        assert all(
            v == getattr(instance, k)
            for k, v in self.update_data.items()
        )


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
                       BaseUpdateViewTest):
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
        response = self.client.put(url, self.update_data)

        assert response.status_code == status.HTTP_200_OK, str(response.data())
        assert count + 1 == self.model.objects.count()
        assert self.model.objects.filter(id=self.instance.id).exists()
        assert self.model.objects.get(id=self.instance.id).archived
        assert response.json() == self.serializer(self.model.objects.last()).data

    def test_partial_update(self):
        count = self.model.objects.count()
        url = reverse(self.basename + '-detail', args=[self.instance.id])
        response = self.client.patch(url, self.update_data)


        assert response.status_code == status.HTTP_200_OK, str(response.json())
        assert count + 1 == self.model.objects.count()
        assert self.model.objects.filter(id=self.instance.id).exists()
        assert self.model.objects.get(id=self.instance.id).archived
        assert response.json() == self.serializer(self.model.objects.last()).data

    def test_archive(self):
        url = reverse(self.basename + '-archive', args=[self.instance.id])
        response = self.client.put(url)

        assert response.status_code == status.HTTP_200_OK
        assert self.model.objects.get(id=self.instance.id).archived


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
