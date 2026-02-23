from rest_framework import serializers
from ed_bgs.models import StateInMinorFaction, State

class StateInMinorFactionBaseInformationSerializer(serializers.ModelSerializer):

    state = serializers.SlugRelatedField(
        queryset=State.objects.all(),
        slug_field='name',
    )
    phase = serializers.CharField(source='get_phase_display', read_only=True)

    class Meta:
        model = StateInMinorFaction
        fields = ['id', 'state', 'phase']
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'created_by': {'read_only': True},
            'updated_by': {'read_only': True},
        }


class StateInMinorFactionSerializer(StateInMinorFactionBaseInformationSerializer):
    class Meta(StateInMinorFactionBaseInformationSerializer.Meta):
        fields = None
        exclude = ['minorFaction']
