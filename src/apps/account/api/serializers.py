from rest_framework import serializers

from src.apps.account.models import User
from src.core.utils import ExceptionWithMessage


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=120)
    full_name = serializers.CharField(max_length=120, allow_null=True, allow_blank=True, required=False)
    password = serializers.CharField(max_length=120, write_only=True)
    is_admin = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'full_name', 'is_admin')

    def create(self, validated_data: dict) -> User:
        try:
            User.objects.get(username=validated_data['username'])
            raise ExceptionWithMessage('Такой пользователь уже существует')
        except User.DoesNotExist:
            return User.objects.create_user(**validated_data)
