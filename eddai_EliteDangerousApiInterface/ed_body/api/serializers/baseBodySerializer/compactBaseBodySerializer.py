from rest_framework import serializers
from ed_body.models import BaseBody

class CompactBaseBodySerializer(serializers.ModelSerializer):

    class Meta:
        model = BaseBody
        fields = ['id', 'name']