from ..baseSerializer import BaseSerializer
from rest_framework import serializers
from ..customFields import  CoordinateListField

from ed_system.models import System

from core.utility import create_or_update_if_time

class BaseJournalSerializer(BaseSerializer):
    StarSystem = serializers.CharField(
        min_length=1,
        source='name',
    )
    StarPos = CoordinateListField(
        source='coordinate',
    )
    timestamp = serializers.DateTimeField(
        input_formats=[
            "%Y-%m-%dT%H:%M:%SZ"
        ],
        source="updated_at"
    )

    def get_objects(self):
        return System.objects.get(name=self.validated_data.get('name'))

    class Meta:
        model = System
        fields = [
            'StarSystem', 'StarPos',
            'timestamp',
        ]