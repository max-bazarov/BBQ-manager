from core.services import BaseService

from .models import Procedure
from .serializers import ProcedureSerializer


class ProcedureService(BaseService):
    model = Procedure
    serializer_class = ProcedureSerializer
    related_name = 'employees'
