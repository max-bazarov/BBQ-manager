from rest_framework import serializers

from .models import Department, Object


class ObjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Object
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = '__all__'
