from __future__ import annotations

from datetime import datetime
from typing import Any, Callable
from urllib.request import Request

from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework_jwt.serializers import JSONWebTokenSerializer, RefreshJSONWebTokenSerializer, VerifyJSONWebTokenSerializer
from rest_framework_jwt.settings import api_settings

from core.views import jwt_response_payload_handler


class JSONWebTokenAPIView(APIView):
    """
    Base API View that various JWT interactions inherit from.
    """

    permission_classes = ()
    authentication_classes = ()

    def get_serializer_context(self) -> dict:
        """
        Extra context provided to the serializer class.
        """
        return {
            "request": self.request,
            "view": self,
        }

    def get_serializer_class(self) -> Serializer:
        """
        Return the class to use for the serializer.
        Defaults to using `self.serializer_class`.
        You may want to override this if you need to provide different
        serializations depending on the incoming request.
        (Eg. admins get full serialization, others get basic serialization)
        """
        assert self.serializer_class is not None, (
            f"'{self.__class__.__name__}' should either include a `serializer_class` attribute, or override the `get_serializer_class()` method."
        )
        return self.serializer_class

    def get_serializer(self, *args: Any, **kwargs: dict[str, Any]) -> Callable:
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_serializer_class()
        kwargs["context"] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def post(self, request: Request, *args: Any, **kwargs: dict[dict, Any]) -> Response:
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        user = serializer.object.get("user") or request.user
        token = serializer.object.get("token")
        response_data = jwt_response_payload_handler(token, user, request)
        response = Response(response_data)
        if api_settings.JWT_AUTH_COOKIE:
            expiration = datetime.now() + api_settings.JWT_EXPIRATION_DELTA
            response.set_cookie(api_settings.JWT_AUTH_COOKIE, token, expires=expiration, httponly=True)
        return response


class ObtainJSONWebToken(JSONWebTokenAPIView):
    """
    API View that receives a POST with a user's username and password.

    Returns a JSON Web Token that can be used for authenticated requests.
    """

    serializer_class = JSONWebTokenSerializer


class VerifyJSONWebToken(JSONWebTokenAPIView):
    """
    API View that checks the veracity of a token, returning the token if it
    is valid.
    """

    serializer_class = VerifyJSONWebTokenSerializer


class RefreshJSONWebToken(JSONWebTokenAPIView):
    """
    API View that returns a refreshed token (with new expiration) based on
    existing token

    If 'orig_iat' field (original issued-at-time) is found, will first check
    if it's within expiration window, then copy it to the new token
    """

    serializer_class = RefreshJSONWebTokenSerializer


obtain_jwt_token = ObtainJSONWebToken.as_view()
refresh_jwt_token = RefreshJSONWebToken.as_view()
verify_jwt_token = VerifyJSONWebToken.as_view()
