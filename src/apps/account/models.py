from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(
            self,
            username: str = None,
            password: str = None,
            full_name: str = None
    ) -> "User":
        if username is None:
            raise TypeError('User must have a username')
        if password is None:
            raise TypeError('User must have a password')

        user = self.model(username=username, full_name=full_name)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username: str, password: str) -> "User":
        if password is None:
            raise TypeError('Superuser must have a password')

        user = self.create_user(username, password)
        user.is_admin = True
        user.is_staff = True
        user.save()

        return user



class User(AbstractBaseUser):
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password']

    username = models.CharField(max_length=120, unique=True)
    full_name = models.CharField(max_length=120, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return self.username

    def has_perm(self, perm, obj=None) -> bool:
        return self.is_admin

    def has_module_perms(self, app_label) -> bool:
        return self.is_admin
