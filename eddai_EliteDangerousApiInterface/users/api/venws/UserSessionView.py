from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from users.api.serializers import UserSessionSerializer


@extend_schema(
    description="Returns session information for the authenticated user.",
    responses={200: UserSessionSerializer},
)
class UserSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSessionSerializer(request.user)
        return Response(serializer.data)
