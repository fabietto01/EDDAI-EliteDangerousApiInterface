from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from users.api.serializers import UserProfileSerializer


@extend_schema(
    description="Retrieve or update non-sensitive profile information for the authenticated user.",
    responses={200: UserProfileSerializer},
)
class UserProfileView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer
    http_method_names = ['get', 'patch']

    def get_object(self):
        return self.request.user
