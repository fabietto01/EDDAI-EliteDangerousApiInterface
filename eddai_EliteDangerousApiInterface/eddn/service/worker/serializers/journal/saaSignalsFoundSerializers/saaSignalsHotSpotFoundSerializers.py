from .saaSignalsBaseFoundSerializers import SAASignalsBaseFoundSerializers
import re

from ...nestedSerializers import HotspotSerializers

from ed_mining.models import Ring
from ed_body.models import BaseBody

from core.utility import create_or_update_if_time, in_list_models

class SAASignalsHotSpotFoundSerializers(SAASignalsBaseFoundSerializers):
    Signals = HotspotSerializers(
        many=True
    )

    def _get_body_name(self, validated_data:dict) -> str:
        regix = r"\s[A-Z]\sRing$"
        return re.sub(
            regix, "", validated_data.get('BodyName'), 0, 
        )
    
    def _get_class_body(self, validated_data):
        return BaseBody

    def run_update_hotspot(self, instance:Ring, validated_data:dict) -> None:
        serializer = HotspotSerializers(
            data=self.initial_data.get('Signals', []), many=True,
            context={'ring': instance}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(
            created_by=validated_data.get('created_by'),
            updated_by=validated_data.get('updated_by'),
            updated_at=validated_data.get('updated_at'),
            ring=instance,
        )

    def create_dipendent(self, instance:Ring, validated_data:dict) -> None:
        self.run_update_hotspot(instance, validated_data)

    def update_dipendent(self, instance:Ring, validated_data:dict) -> None:
        self.run_update_hotspot(instance, validated_data)

    def update_or_create(self, validated_data:dict) -> Ring:
        palent = super().update_or_create(validated_data)
        def_create_dipendent = lambda instance: self.create_dipendent(instance, validated_data)
        def_update_dipendent = lambda instance: self.update_dipendent(instance, validated_data)
        ring, create = create_or_update_if_time(
            Ring, time=self.get_time(),
            defaults={},
            defaults_create=self.get_data_defaults_create(validated_data),
            defaults_update=self.get_data_defaults_update(validated_data),
            create_function=def_create_dipendent,
            update_function=def_update_dipendent,
            body=palent,
            name=validated_data.get('BodyName'),
        )
        return ring
