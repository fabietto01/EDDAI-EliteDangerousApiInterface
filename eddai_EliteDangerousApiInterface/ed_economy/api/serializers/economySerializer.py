from rest_framework import serializers
from ed_economy.models import Economy

class EconomyBasicInformationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Economy model.
    """

    class Meta:
        model = Economy
        fields = ['id', 'name']

class EconomySerializer(EconomyBasicInformationSerializer):
    class Meta(EconomyBasicInformationSerializer.Meta):
        fields = None
        exclude = ['_eddn', 'eddn']