from rest_framework import serializers
from ed_bgs.models import MinorFaction, Faction, Government

class MinorFactionSerializer(serializers.ModelSerializer):

    allegiance = serializers.SlugRelatedField(
        queryset=Faction.objects.all(),
        slug_field='name',
    )

    government = serializers.SlugRelatedField(
        queryset=Government.objects.all(),
        slug_field='name',
    )

    class Meta:
        model = MinorFaction
        fields = '__all__'
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'created_by': {'read_only': True},
            'updated_by': {'read_only': True},
        }
