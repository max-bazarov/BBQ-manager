from rest_framework import serializers

from procedures.serializers import ProcedureSerializer

from .models import Employee, MasterProcedure


class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = '__all__'


class MasterProcedureSerializer(serializers.ModelSerializer):

    class Meta:
        model = MasterProcedure
        fields = '__all__'


class MasterProcedureListSerializer(serializers.ModelSerializer):

    procedure = ProcedureSerializer()
    employee = EmployeeSerializer()

    class Meta:
        model = MasterProcedure
        fields = '__all__'
