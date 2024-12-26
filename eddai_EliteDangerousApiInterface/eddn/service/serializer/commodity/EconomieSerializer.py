from rest_framework import serializers

from ed_economy.models import Economy

from core.api.fields import CacheSlugRelatedField

class EconomieSerializer(serializers.Serializer):
    name = CacheSlugRelatedField(
        queryset=Economy.objects.all(),
        slug_field='eddn',
    )
    proportion = serializers.FloatField(
        min_value=0,
    )
    
    class Meta:
        model = Economy