from rest_framework import serializers

class MixinEDDNSerializer:
    pass
    
class BaseListSerializer(MixinEDDNSerializer, serializers.ListSerializer):

    def create(self, validated_data):
        raise NotImplementedError("create method not implemented")
    
    def update(self, instance, validated_data):
        raise NotImplementedError("update method not implemented")
    
    def get_fields_materilFaciotn(self, model=None):
        if not model:
            model = self.Meta.model
        return [field.name for field in model._meta.fields]

class BaseSerializer(MixinEDDNSerializer, serializers.ModelSerializer):
    
    def get_objects(self):
        raise NotImplementedError("get_objects() must be implemented")
    
    def is_valid(self, *, raise_exception=False):
        valid = super().is_valid(raise_exception=raise_exception)
        if valid:
            ModelClass = self.Meta.model
            try:
                self.instance = self.get_objects()
            except ModelClass.DoesNotExist:
                pass
        return valid
    
    def update(self, instance, validated_data):
        validated_data.pop('created_by', None)
        if instance.updated_at < validated_data.get('updated_at'):
            instance = super().update(instance, validated_data)
        return super().update(instance, validated_data)