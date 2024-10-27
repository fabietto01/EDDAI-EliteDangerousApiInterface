from rest_framework import serializers
from eddn.service.serializer.journals.scan.BaseScanSerializer import BaseScanSerializer

from core.utility import get_values_list_or_default, get_or_none
from core.api.fields import CacheSlugRelatedField
from django.db import OperationalError, ProgrammingError

from ed_body.models import Star, StarLuminosity, StarType

class StarScanSerializer(BaseScanSerializer):
    
    AbsoluteMagnitude = serializers.FloatField(
        min_value=0,
    )
    Age_MY = serializers.FloatField(
        min_value=0,
    )
    Luminosity = CacheSlugRelatedField(
        queryset=StarLuminosity.objects.all(),
        slug_field='eddn',
    )
    StarType = CacheSlugRelatedField(
        queryset=StarType.objects.all(),
        slug_field='eddn',
    )

    StellarMass = serializers.FloatField(
        min_value=0,
    )
    Subclass = serializers.IntegerField(
        min_value=0,
        max_value=9,
    )

    def set_data_defaults(self, validated_data: dict) -> dict:
        defaults = super().set_data_defaults(validated_data)
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