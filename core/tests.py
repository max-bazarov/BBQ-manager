class BaseCreateServiceTests:

    def test_create(self):
        count = self.model.objects.count()
        instance = self.create_service.execute(self.data)

        assert count + 1 == self.model.objects.count(), (
            f'{self.create_service.__class__.__name__} does not create instance'
        )
        assert isinstance(instance, self.model), (
            f'{self.create_service.__class__.__name__} create method does not return instance'
        )
