from rest_framework import serializers

from ed_station.models import ServiceInStation, Service

class ServiceInStationListSerializer(serializers.ListSerializer):

    def validate(self, attrs):
        try:
            station_pk:int = self.context["station_pk"]
            queryset = ServiceInStation.objects.filter(staion_id=station_pk)
            if queryset.filter(service__in=[item.service for item in attrs]).exists():
                raise serializers.ValidationError(f"")
        except KeyError:
            from rest_framework import status
            raise serializers.ValidationError('An internal server error occurred', code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return attrs
    
    def create(self, validated_data):
        serviceInStation = [ServiceInStation(**item) for item in validated_data]
        return ServiceInStation.objects.bulk_create(serviceInStation)
    
class ServiceInStationBasicInformation(serializers.ModelSerializer):
    """
    Serializer for the ServiceInStation model.
    """

    service = serializers.SlugRelatedField(
        queryset=Service.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = ServiceInStation
        fields = ['id', 'service']
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'created_by': {'read_only': True},
            'updated_by': {'read_only': True},
        }

class ServiceInStationSerializer(ServiceInStationBasicInformation):
    """
    Serializer for the ServiceInStation model.
    """

    class Meta(ServiceInStationBasicInformation.Meta):
        model = ServiceInStation
        fields = None
        exclude = ['station']
        list_serializer_class = ServiceInStationListSerializer