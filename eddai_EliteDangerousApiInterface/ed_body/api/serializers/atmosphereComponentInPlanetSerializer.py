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
    
    def validate(self, attrs):
        try:
            planet_pk:int = self.context['planet_pk']
            queryset = AtmosphereComponentInPlanet.objects.filter(planet_id=planet_pk)
            percent = sum([item['percent'] for item in attrs])
            if queryset.aggregate(Sum('percent', default=0))['percent__sum'] + percent > AtmosphereComponentInPlanet.max_percent():
                raise serializers.ValidationError(f'the sum of the percent for the planet cannot be greater than {AtmosphereComponentInPlanet.max_percent()}')
        except KeyError:
            from rest_framework import status
            raise serializers.ValidationError('An internal server error occurred', code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return attrs
    
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
            planet_pk:int = self.context['planet_pk']
            queryset = AtmosphereComponentInPlanet.objects.filter(planet_id=planet_pk)
            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)
            if queryset.aggregate(Sum('percent', default=0))['percent__sum'] + attrs['percent'] > AtmosphereComponentInPlanet.max_percent():
                raise serializers.ValidationError(f'the sum of the percent for the planet cannot be greater than {AtmosphereComponentInPlanet.max_percent()}')
        except KeyError:
            from rest_framework import status
            raise serializers.ValidationError('An internal server error occurred', code=status.HTTP_500_INTERNAL_SERVER_ERROR)
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