from rest_framework import serializers

from ed_bgs.models import State

class StateListSerializer(serializers.ListSerializer):

    def validate(self, attrs):
        count = len(attrs)
        if count < 1:
            raise serializers.ValidationError(f"too few states: {count}")
        return super().validate(attrs)

class StateSerializer(serializers.Serializer):
    State = serializers.SlugRelatedField(
        queryset=State.objects.exclude(type=State.TypeChoices.HAPPINESS.value),
        slug_field='eddn',
    )

    class Meta:
        list_serializer_class = StateListSerializer