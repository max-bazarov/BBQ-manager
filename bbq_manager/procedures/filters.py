from django_filters import rest_framework as filters

from .models import Procedure


class ProcedureFilter(filters.FilterSet):
    object = filters.NumberFilter(field_name="department", lookup_expr='object')

    class Meta:
        model = Procedure
        fields = ['department']
