from rest_framework import serializers

from inventory.models import Material


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'unit', 'price')
        model = Material
