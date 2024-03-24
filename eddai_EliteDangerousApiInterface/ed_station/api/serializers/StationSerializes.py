from rest_framework import serializers
from django.db import OperationalError, ProgrammingError
import uuid

from ed_station.api.serializers import NestedServiceModelSerializes

from ed_station.models import Station, Service
from ed_economy.models import Economy


from core.api.fields import CacheChoiceField
from core.utility import get_values_list_or_default

class StationModelSerializes(serializers.ModelSerializer):
    """
    serializer dedicato alla visualizaione di stazioni
    """

    service = NestedServiceModelSerializes(many=True, read_only=True)
    service_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=Service.objects.all(),
        source='service',
        many=True
    )

    class Meta:
        model = Station
        fields = '__all__'