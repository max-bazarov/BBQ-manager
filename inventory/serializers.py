from rest_framework import serializers

from inventory.models import Material


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Material
