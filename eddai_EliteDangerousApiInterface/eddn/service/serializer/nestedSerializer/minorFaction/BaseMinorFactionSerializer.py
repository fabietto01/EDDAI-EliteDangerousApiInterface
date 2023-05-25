from eddn.service.serializer.nestedSerializer.BaseSecondarySerializer import BaseNestedSerializer
from rest_framework import serializers

class BaseMinorFactionSerializer(BaseNestedSerializer):
    Name = serializers.CharField(
        min_length=1,
    )