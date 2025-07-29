from .saaSignalsBaseFoundSerializers import SAASignalsBaseFoundSerializers

from ...nestedSerializers import SignalSerializers, SampleSerializers

from ed_body.models import Planet
from ed_exploration.models import SampleSignals

class SAASignalsFoundSerializers(SAASignalsBaseFoundSerializers):
    Signals = SignalSerializers(
        many=True
    )
    Genuses = SampleSerializers(
        many=True,
        required=False,
    )
    
    def _get_body_name(self, validated_data:dict) -> str:
        return validated_data.get('BodyName')
    
    def _get_class_body(self, validated_data):
        return Planet
    
    def run_update_signals(self, instance:Planet, validated_data:dict) -> None:
        serializer = SignalSerializers(
            data=self.initial_data.get('Signals', []), many=True,
            context={'planet': instance}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(
            created_by=validated_data.get('created_by'),
            updated_by=validated_data.get('updated_by'),
            updated_at=validated_data.get('updated_at'),
            planet=instance,
        )

    def run_update_genuses(self, instance:Planet, validated_data:dict) -> None:
        if self.validated_data.get('Genuses', []):
            serializer = SampleSerializers(
                data=self.initial_data.get('Genuses', []), many=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(
                created_by=validated_data.get('created_by'),
                updated_by=validated_data.get('updated_by'),
                updated_at=validated_data.get('updated_at'),
                planet=instance,
            )

    def create_dipendent(self, instance:Planet, validated_data:dict) -> None:
        self.run_update_signals(instance, validated_data)
        self.run_update_genuses(instance, validated_data)

    def update_dipendent(self, instance:Planet, validated_data:dict) -> None:
        self.run_update_signals(instance, validated_data)
        self.run_update_genuses(instance, validated_data)
    
    def update_or_create(self, validated_data:dict):
        def_create_dipendent = lambda instance: self.create_dipendent(instance, validated_data)
        def_update_dipendent = lambda instance: self.update_dipendent(instance, validated_data)
        return super().update_or_create(validated_data, def_update_dipendent, def_create_dipendent)
        