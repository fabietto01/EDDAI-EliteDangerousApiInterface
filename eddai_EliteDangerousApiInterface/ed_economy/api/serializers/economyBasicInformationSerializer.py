from rest_framework.serializers import ModelSerializer

from ed_economy.models import Economy

class EconomyBasicInformationSerializer(ModelSerializer):
    """
    Serializer for the Economy model.
    """

    class Meta:
        model = Economy
        fields = ['id', 'name']