from core.services import BaseService

from .models import Employee, MasterProcedure
from .serializers import EmployeeSerializer, MasterProcedureSerializer


class EmployeeService(BaseService):
    model = Employee
    serializer_class = EmployeeSerializer
    related_name = 'procedures'


class MasterProcedureService(BaseService):
    model = MasterProcedure
    serializer_class = MasterProcedureSerializer
    related_name = 'purchases'
    archivable_relation = False
