from rest_framework import serializers

from objects.serializers import DepartmentSerializer

from .models import Procedure


class ProcedureSerializer(serializers.ModelSerializer):

    class Meta:
        model = Procedure
        fields = '__all__'


class ProcedureListSerializer(ProcedureSerializer):

    department = DepartmentSerializer()
