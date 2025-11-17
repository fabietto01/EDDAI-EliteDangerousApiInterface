from rest_framework import serializers
from django.db.models import Sum

from ed_material.models import MaterialInPlanet, Material

class ListCompactedMaterialInPlanetSerializer(serializers.ListSerializer):
    """
    ListCompactedMaterialInPlanetSerializer is used to increase the efficiency of data insertion 
    regarding the composition of a planet's materials. This serializer leverages Django's bulk_create method 
    to insert multiple MaterialInPlanet instances in a single query, improving performance 
    when handling large datasets.
    """
    
    def validate(self, attrs):
        try:
            planet_pk:int = self.context['planet_pk']
            queryset = MaterialInPlanet.objects.filter(planet_id=planet_pk)
            percent = sum([item['percent'] for item in attrs])
            if queryset.aggregate(Sum('percent', default=0))['percent__sum'] + percent > 100:
                raise serializers.ValidationError('the sum of the percent for the planet cannot be greater than 100')
        except KeyError:
            from rest_framework import status
            raise serializers.ValidationError('An internal server error occurred', code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return attrs
    
    def create(self, validated_data):
        materials = [MaterialInPlanet(**item) for item in validated_data]
        return MaterialInPlanet.objects.bulk_create(materials)

class CompactedMaterialInPlanetSerializer(serializers.ModelSerializer):
    """
    CompactedMaterialInPlanetSerializer is a serializer for the MaterialInPlanet model.
    Attributes:
        Meta (type): The metadata class for the serializer.
    """

    material = serializers.SlugRelatedField(
        queryset=Material.objects.all(),
        slug_field='name'
    )

    def validate(self, attrs):
        try:
            planet_pk:int = self.context['planet_pk']
            queryset = MaterialInPlanet.objects.filter(planet_id=planet_pk)
            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)
            if queryset.aggregate(Sum('percent', default=0))['percent__sum'] + attrs['percent'] > 100:
                raise serializers.ValidationError('the sum of the percent for the planet cannot be greater than 100')
        except KeyError:
            from rest_framework import status
            raise serializers.ValidationError('An internal server error occurred', code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return attrs

    class Meta:
        model = MaterialInPlanet
        fields = ['material', 'percent']

class MaterialInPlanetSerializer(CompactedMaterialInPlanetSerializer):
    """
    MaterialInPlanetSerializer is a serializer for the MaterialInPlanet model.
    Attributes:
        Meta (type): The metadata class for the serializer.
    """

    class Meta(CompactedMaterialInPlanetSerializer.Meta):
        model = MaterialInPlanet
        fields = None
        exclude = ['material', 'planet']
        read_only_fields = [
            'created_at','updated_at',
            'created_by','updated_by',
            'planet'
        ]
        list_serializer_class = ListCompactedMaterialInPlanetSerializer
