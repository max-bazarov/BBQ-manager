from rest_framework import serializers

from .models import Employee, MasterProcedure


class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = '__all__'


class MasterProcedureSerializer(serializers.ModelSerializer):

    class Meta:
        model = MasterProcedure
        fields = '__all__'
