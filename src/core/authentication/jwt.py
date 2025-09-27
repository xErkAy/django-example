from __future__ import annotations

from urllib.request import Request

import jwt
from django.contrib.auth import get_user_model
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings

from apps.account.models import User
from apps.authentication.exceptions import AuthenticationFailed, DecodeSignature, ExpiredSignature, InvalidPayload, InvalidSignature, JWTTokenNotFound

jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER


class CustomJWTAuthentication(JSONWebTokenAuthentication):
    def authenticate(self, request: Request | None = None, token: str | None = None) -> list[User, str]:
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
