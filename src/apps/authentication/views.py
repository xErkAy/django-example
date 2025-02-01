from typing import Callable, Any
from urllib.request import Request

import jwt

from datetime import datetime

from django.contrib.auth import get_user_model
from rest_framework.serializers import Serializer

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.serializers import (
    JSONWebTokenSerializer,
    RefreshJSONWebTokenSerializer,
    VerifyJSONWebTokenSerializer
)

from src.apps.account.models import User
from src.apps.authentication.exceptions import (
    JWTTokenNotFound,
    ExpiredSignature,
    DecodeSignature,
    AuthenticationFailed,
    InvalidSignature,
    InvalidPayload
)

jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER


class CustomJWTAuthentication(JSONWebTokenAuthentication):

    def authenticate(self, request: Request = None, token: str = None) -> list[User, str]:
        if request is None and token is None:
            raise JWTTokenNotFound()

        if token is None:
            token = self.get_jwt_value(request)

        if token is None:
            raise JWTTokenNotFound()

        try:
            payload = jwt_decode_handler(token)
        except jwt.ExpiredSignature:
            raise ExpiredSignature()
        except jwt.DecodeError:
            raise DecodeSignature()
        except jwt.InvalidTokenError:
            raise AuthenticationFailed()

        user = self._authenticate_credentials(payload)
        return user, token

    @staticmethod
    def _authenticate_credentials(payload: dict) -> User:
        model = get_user_model()
        username = jwt_get_username_from_payload(payload)
        if username:
            try:
                user = model.objects.get(username=username)
            except model.DoesNotExist:
                raise InvalidSignature()
        else:
            raise InvalidPayload()

        return user


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
            'request': self.request,
            'view': self,
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
            "'%s' should either include a `serializer_class` attribute, "
            "or override the `get_serializer_class()` method."
            % self.__class__.__name__)
        return self.serializer_class

    def get_serializer(self, *args, **kwargs) -> Callable:
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def post(self, request: Request, *args: Any, **kwargs: dict[dict, Any]) -> Response:
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        user = serializer.object.get('user') or request.user
        token = serializer.object.get('token')
        response_data = jwt_response_payload_handler(token, user, request)
        response = Response(response_data)
        if api_settings.JWT_AUTH_COOKIE:
            expiration = (datetime.now() +
                          api_settings.JWT_EXPIRATION_DELTA)
            response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                token,
                                expires=expiration,
                                httponly=True)
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
