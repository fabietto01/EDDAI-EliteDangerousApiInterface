from rest_framework import serializers
from eddn.service.journals.scan.BaseScanSerializer import BaseScanSerializer

from core.utility import update_or_create_if_time, get_values_list_or_default, get_or_none
from django.db import OperationalError, ProgrammingError

class PlanetScan(BaseScanSerializer):
    pass