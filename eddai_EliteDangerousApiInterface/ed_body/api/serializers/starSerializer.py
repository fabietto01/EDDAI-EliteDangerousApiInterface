from rest_framework import serializers
from .baseBodySerializer import BaseBodySerializer

from ed_body.models import (
    Star
)

from ed_core.api.serializers.DistanceSerializer import DistanceSerializer

class StarSerializer(BaseBodySerializer):
    """
    StarSerializer is a serializer for the Star model.
    Attributes:
        Meta (type): The metadata class for the serializer.
    """
    class Meta(BaseBodySerializer.Meta):
        model = Star

class StarDistanceSerializer(StarSerializer, DistanceSerializer):
    class Meta(StarSerializer.Meta):
        pass