from rest_framework import serializers
from ed_body.models import BaseBody
from ed_core.api.serializers.DistanceSerializer import DistanceSerializer

from ed_system.api.serializers import SystemBasicInformation, System

class BaseBodySerializer(serializers.ModelSerializer):
    """
    BaseBodySerializer is a serializer for the BaseBody model.
    Attributes:
        Meta (type): The metadata class for the serializer.
    """

    system = SystemBasicInformation(read_only=True)
    system_id = serializers.PrimaryKeyRelatedField(
        queryset=System.objects.all(),
        write_only=True,
        source='system',
    )

    class Meta:
        model = BaseBody
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'created_by': {'read_only': True},
            'updated_by': {'read_only': True},
        }
        fields = "__all__"

class BaseBodyBasicInformation(BaseBodySerializer):

    class Meta(BaseBodySerializer.Meta):
        fields = ['id', 'name']

class BaseBodyDistanceSerializer(BaseBodySerializer, DistanceSerializer):
    class Meta(BaseBodySerializer.Meta):
        pass