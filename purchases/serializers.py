from rest_framework import serializers

from .models import UsedMaterial


class UsedMaterialSerializer(serializers.ModelSerializer):

    class Meta:
        model = UsedMaterial
        fields = '__all__'