from core.services import BaseService

from .models import Employee
from .serializers import EmployeeSerializer


class NewEmployeeService(BaseService):
    model = Employee
    serializer_class = EmployeeSerializer
    related_name = 'procedures'
