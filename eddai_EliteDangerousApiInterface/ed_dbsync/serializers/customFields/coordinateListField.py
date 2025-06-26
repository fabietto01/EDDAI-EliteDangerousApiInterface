from rest_framework import serializers
from django.contrib.gis.geos import Point

class CoordinateListField(serializers.Field):
    def to_internal_value(self, data):
        if not isinstance(data, list) or len(data) != 3:
            raise serializers.ValidationError('This field requires a list of three float values.')
        
        try:
            x, y, z = map(float, data)
        except ValueError:
            raise serializers.ValidationError('All elements in the list must be float values.')
        
        return Point(x, y, z)

    def to_representation(self, value):
        if not isinstance(value, Point):
            raise serializers.ValidationError('Expected a Point object.')
        
        return [value.x, value.y, value.z]