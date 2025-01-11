from rest_framework import serializers
from django.db.models import Sum

from ed_body.models import AtmosphereComponentInPlanet, AtmosphereComponent

class ListCompactedAtmosphereComponentInPlanetSerializer(serializers.ListSerializer):
    """
    ListCompactedAtmosphereComponentInPlanetSerializer is used to increase the efficiency of data insertion 
    regarding the composition of a planet's atmosphere. This serializer leverages Django's bulk_create method 
    to insert multiple AtmosphereComponentInPlanet instances in a single query, improving performance 
    when handling large datasets.
    """
    
    def create(self, validated_data):
        atmosphereComponent = [AtmosphereComponentInPlanet(**item) for item in validated_data]
        return AtmosphereComponentInPlanet.objects.bulk_create(atmosphereComponent)

class CompactedAtmosphereComponentInPlanetSerializer(serializers.ModelSerializer):
    """
    CompactedAtmosphereComponentInPlanetSerializer is a serializer for the AtmosphereComponentInPlanet model.
    Attributes:
        Meta (type): The metadata class for the serializer.
    """

    atmosphere = serializers.SlugRelatedField(
        queryset=AtmosphereComponent.objects.all(),
        source='atmosphere_component',
        slug_field='name'
    )

    def validate(self, attrs):
        try:
            planet_pk:int = self.context.get('planet_pk')
            queryset = AtmosphereComponentInPlanet.objects.filter(planet_id=planet_pk)
            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)
            if queryset.aggregate(Sum('percent', default=0))['percent__sum'] + attrs['percent'] > 100:
                raise serializers.ValidationError('the sum of the percent for the planet cannot be greater than 100')
        except KeyError:
            raise serializers.ValidationError('planet_pk is required') 
        return attrs

    class Meta:
        model = AtmosphereComponentInPlanet
        fields = ['atmosphere', 'percent']

class AtmosphereComponentInPlanetSerializer(CompactedAtmosphereComponentInPlanetSerializer):
    """
    AtmosphereComponentInPlanetSerializer is a serializer for the AtmosphereComponentInPlanet model.
    Attributes:
        Meta (type): The metadata class for the serializer.
    """

    class Meta(CompactedAtmosphereComponentInPlanetSerializer.Meta):
        model = AtmosphereComponentInPlanet
        fields = None
        exclude = ['atmosphere_component', 'planet']
        read_only_fields = [
            'created_at','updated_at',
            'created_by','updated_by',
            'planet'
        ]
        list_serializer_class = ListCompactedAtmosphereComponentInPlanetSerializer