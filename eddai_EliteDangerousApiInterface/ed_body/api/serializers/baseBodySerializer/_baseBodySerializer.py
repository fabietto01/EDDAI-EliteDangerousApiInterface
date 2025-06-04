from rest_framework.serializers import PrimaryKeyRelatedField

from .compactBaseBodySerializer import CompactBaseBodySerializer
from ed_system.api.serializers import SystemBasicInformation, System

class _BaseBodySerializer(CompactBaseBodySerializer):
    """
    BaseBodySerializer is a serializer for the BaseBody model.
    Attributes:
        Meta (type): The metadata class for the serializer.
    """

    system = SystemBasicInformation(read_only=True)
    system_id = PrimaryKeyRelatedField(
        queryset=System.objects.all(),
        write_only=True,
        source='system',
    )

    class Meta(CompactBaseBodySerializer.Meta):
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'created_by': {'read_only': True},
            'updated_by': {'read_only': True},
        }
        fields = "__all__"