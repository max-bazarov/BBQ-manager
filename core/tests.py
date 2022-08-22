from typing import Any

from django.db.models import Model
from django.urls import reverse
from rest_framework import status
from rest_framework.serializers import Serializer


class BaseCreateServiceTest:

    def test_create(self):
        count = self.model.objects.count()
        instance = self.create_service.execute(self.data)

        assert count + 1 == self.model.objects.count(), (
            f'{self.create_service.__class__.__name__} does not create instance'
        )
        assert isinstance(instance, self.model), (
            f'{self.create_service.__class__.__name__} create method does not return instance'
        )
        for k, v in self.data.items():
            assert v == getattr(instance, k)


class BaseDestroyServiceTest:

    def test_destroy(self):
        count = self.model.objects.count()
        instance = self.model.objects.first()

        self.destroy_service.execute({'id': instance.id})
        assert count - 1 == self.model.objects.count(), ('fail')


class BaseArchiveServiceTest:

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
            f'is not equal to old instance data'
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
    model: type[Model]
    serializer: type[Serializer]
    instance: Model
    data: dict[str, str]
    basename: str


class BaseCreateViewTest(BaseViewTest):

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

    def test_retrieve_view(self):
        url = reverse(self.basename + '-detail', args=[self.instance.id])
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == self.serializer(self.instance).data


class BaseListViewTest(BaseViewTest):

    def test_list_view(self):
        url = reverse(self.basename + '-list')
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == self.serializer(self.model.objects.all(), many=True).data


class BaseUpdateViewTest(BaseViewTest):
    update_data: dict[str, Any]

    def test_update_view(self):
        count = self.model.objects.count()
        url = reverse(self.basename + '-detail', args=[self.instance.id])
        response = self.client.put(url, self.update_data)
        instance = self.model.objects.get(id=self.instance.pk)

        assert response.status_code == status.HTTP_200_OK
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
    pass


class BaseArchiveViewTest(BaseViewTest):
    update_data: dict[str, Any]

    def test_update(self):
        count = self.model.objects.count()
        url = reverse(self.basename + '-detail', args=[self.instance.id])
        response = self.client.put(url, self.update_data)

        assert response.status_code == status.HTTP_200_OK
        assert count + 1 == self.model.objects.count()
        assert self.model.objects.filter(id=self.instance.id).exists()
        assert self.model.objects.get(id=self.instance.id).archived
        assert response.json() == self.serializer(self.model.objects.last()).data

    def test_partial_update(self):
        count = self.model.objects.count()
        url = reverse(self.basename + '-detail', args=[self.instance.id])
        response = self.client.put(url, self.update_data)

        assert response.status_code == status.HTTP_200_OK
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
    pass
