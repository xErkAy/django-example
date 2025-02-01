from typing import Any

from django.contrib.auth import login

from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from src.apps.account.models import User
from src.apps.account.api.serializers import UserSerializer
from src.apps.authentication.exceptions import AuthenticationFailed
from src.apps.authentication.views import (
    JSONWebTokenAPIView,
    jwt_payload_handler,
    jwt_encode_handler
)


class ProfileAPIView(APIView):
    def get(self, request: Request, *args: Any, **kwargs: dict[str, Any]) -> Response:
        # authentication = CustomJWTAuthentication()
        # # user, token = authentication.authenticate(request=request)
        return Response(UserSerializer(request.user).data)


class AuthenticationAPIView(JSONWebTokenAPIView):
    serializer_class = UserSerializer

    def post(self, request: Request, *args: Any, **kwargs: dict[str, Any]) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self._get_user(serializer.validated_data)
        if not user.check_password(serializer.validated_data['password']):
            raise AuthenticationFailed('Неверный логин или пароль')

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        try:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        except Exception:
            raise AuthenticationFailed('Ошибка авторизации пользователя')

        # payload['token'] = token
        response = self.serializer_class(user).data
        response['token'] = token

        return Response(response, status=status.HTTP_200_OK)

    def _get_user(self, data: dict) -> User:
        try:
            user = User.objects.get(username=data['username'])
            return user
        except User.DoesNotExist:
            raise AuthenticationFailed('Неверный логин или пароль')




class RegistrationAPIView(CreateAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = UserSerializer

    def post(self, request: Request, *args: Any, **kwargs: dict[str, Any]) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'success': True}, status=status.HTTP_200_OK)
