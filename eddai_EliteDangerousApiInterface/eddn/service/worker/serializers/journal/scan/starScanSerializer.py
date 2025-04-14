from rest_framework import serializers
from .baseScanSerializer import BaseScanSerializer

from ed_body.models import Star, StarLuminosity, StarType

class StarScanSerializer(BaseScanSerializer):
    AbsoluteMagnitude = serializers.FloatField(
        min_value=-1,
    )
    Age_MY = serializers.FloatField(
        min_value=0,
    )
    Luminosity = serializers.SlugRelatedField(
        queryset=StarLuminosity.objects.all(),
        slug_field='name',
    )
    StarType = serializers.SlugRelatedField(
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

    def set_data_defaults_body(self, validated_data: dict) -> dict:
        defaults = super().set_data_defaults_body(validated_data)
        defaults.update({
            'absoluteMagnitude': validated_data.get('AbsoluteMagnitude'),
            'age': validated_data.get('Age_MY'),
            'luminosity':validated_data.get('Luminosity'),
            'starType': validated_data.get('StarType'),
            'stellarMass': validated_data.get('StellarMass'),
            'subclass': validated_data.get('Subclass'),
        })
        return defaults 
    
    class Meta:
        model = Star