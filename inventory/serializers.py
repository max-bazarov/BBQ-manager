from rest_framework import serializers

from inventory.models import Material


class MaterialSerializer(serializers.ModelSerializer):
    """Сериализатор для материала"""
    class Meta:
        fields = ('name', 'unit', 'price')
        model = Material
