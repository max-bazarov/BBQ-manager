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
