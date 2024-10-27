from rest_framework import serializers
from ..customFields import CustomCacheSlugRelatedField

from ed_economy.models import Economy

class EconomySerializer(serializers.Serializer):
    Name = CustomCacheSlugRelatedField(
        queryset=Economy.objects.all(),
        slug_field='eddn',
    )