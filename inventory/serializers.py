from rest_framework import serializers

from inventory.models import Material, ProductMaterial, Stock


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Material


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Stock


class StockRemainSerializer(serializers.ModelSerializer):
    amount = serializers.IntegerField()

    class Meta:
        fields = '__all__'
        model = Material


class ProductMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = ProductMaterial
