from rest_framework.exceptions import APIException
from django.utils.translation import gettext_lazy as _


class AuthenticationFailed(APIException):
    status_code = 401
    default_detail = _('Authentication failed')


class InvalidUsernameOrPassword(APIException):
    status_code = 401
    default_detail = _('Invalid username or password')


class ExpiredSignature(APIException):
    status_code = 401
    default_detail = _('Signature has expired')


class DecodeSignature(APIException):
    status_code = 401
    default_detail = _('Error decoding signature')


class InvalidSignature(APIException):
    status_code = 401
    default_detail = _('Invalid signature')


class InvalidPayload(APIException):
    status_code = 401
    default_detail = _('Invalid payload')


class JWTTokenNotFound(APIException):
    status_code = 401
    default_detail = _('Authorization token has not been found')
