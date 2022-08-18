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
