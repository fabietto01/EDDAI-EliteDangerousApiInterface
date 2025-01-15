from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import ModelViewSet

class OwnerAndDateModelViewSet(ModelViewSet):
    """
    OwnerAndDateModelViewSet is a custom viewset that extends the ModelViewSet class.
    It overrides the perform_create and perform_update methods to automatically set
    the created_by and updated_by fields to the current user.
    Methods:
        perform_create(serializer: OwnerAndDateModels):
            Saves the serializer with the created_by and updated_by fields set to the current user.
        perform_update(serializer: OwnerAndDateModels):
            Saves the serializer with the updated_by field set to the current user.
    """
    
    def perform_create(self, serializer:BaseSerializer):
        user = self.request.user
        serializer.save(
            created_by=user,
            updated_by=user
        )
    
    def perform_update(self, serializer:BaseSerializer):
        user = self.request.user
        serializer.save(
            updated_by=user
        )