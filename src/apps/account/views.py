from typing import Any

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.account.api.serializers import UserSerializer


class ProfileAPIView(APIView):
    def get(self, request: Request, *args: Any, **kwargs: dict[str, Any]) -> Response:
        return Response(UserSerializer(request.user).data)
