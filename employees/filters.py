from django_filters import rest_framework as filters

from .models import MasterProcedure


class MasterProcedureFilter(filters.FilterSet):

    class Meta:
        model = MasterProcedure
        fields = ['employee', 'procedure']
