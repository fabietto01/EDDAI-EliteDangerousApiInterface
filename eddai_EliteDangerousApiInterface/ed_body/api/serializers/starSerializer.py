from rest_framework import serializers
from .baseBodySerializer._baseBodySerializer import _BaseBodySerializer

from ed_body.models import (
    Star, StarLuminosity, StarType
)

from ed_core.api.serializers.DistanceSerializer import DistanceSerializer
from .starLuminosityserializer import CompactedStarLuminositySerializer
from .starTypeSerializer import CompactedStarTypeSerializer

class StarSerializer(_BaseBodySerializer):
    """
    StarSerializer is a serializer for the Star model.
    Attributes:
        Meta (type): The metadata class for the serializer.
    """

    luminosity = serializers.SlugRelatedField(
        queryset=StarLuminosity.objects.all(),
        slug_field='name'
    )

    starType = serializers.SlugRelatedField(
        queryset=StarType.objects.all(),
        slug_field='name'
    )

    class Meta(_BaseBodySerializer.Meta):
        model = Star

class StarDistanceSerializer(StarSerializer, DistanceSerializer):
    class Meta(StarSerializer.Meta):
        pass