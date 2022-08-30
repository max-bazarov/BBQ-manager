from rest_framework import serializers

from inventory.models import Material, Stock, ProductMaterial


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Material


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Stock


class ProductMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = ProductMaterial
