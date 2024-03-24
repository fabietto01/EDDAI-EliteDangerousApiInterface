from rest_framework import serializers
from eddn.service.serializer.journals.scan.BaseScanSerializer import BaseScanSerializer

from core.utility import get_values_list_or_default, get_or_none
from core.api.fields import CacheChoiceField
from django.db import OperationalError, ProgrammingError

from ed_body.models import Star, StarLuminosity, StarType

import uuid

class StarScanSerializer(BaseScanSerializer):
    
    AbsoluteMagnitude = serializers.FloatField(
        min_value=0,
    )
    Age_MY = serializers.FloatField(
        min_value=0,
    )
    Luminosity = CacheChoiceField(
        fun_choices=lambda: get_values_list_or_default(StarLuminosity, [], (OperationalError, ProgrammingError), 'name', flat=True),
         cache_key=uuid.uuid4(),
    )
    StarType = CacheChoiceField(
        fun_choices=lambda: get_values_list_or_default(StarType, [], (OperationalError, ProgrammingError), 'eddn', flat=True),
         cache_key=uuid.uuid4(),
    )

    StellarMass = serializers.FloatField(
        min_value=0,
    )
    Subclass = serializers.IntegerField(
        min_value=0,
        max_value=9,
    )

    def set_data_defaults(self, validated_data: dict) -> dict:
        defaults = BaseScanSerializer.set_data_defaults(self, validated_data)
        defaults.update({
            'absoluteMagnitude': validated_data.get('AbsoluteMagnitude'),
            'age': validated_data.get('Age_MY'),
            'luminosity': get_or_none(StarLuminosity, name=validated_data.get('Luminosity', None)),
            'starType': get_or_none(StarType, name=validated_data.get('StarType', None)),
            'stellarMass': validated_data.get('StellarMass'),
            'subclass': validated_data.get('Subclass'),
        })
        return defaults

    class Meta:
        model = Star