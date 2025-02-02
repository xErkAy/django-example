from __future__ import annotations

from typing import Any

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, username: str | None = None, password: str | None = None, full_name: str | None = None) -> User:
        if username is None:
            raise TypeError("User must have a username")
        if password is None:
            raise TypeError("User must have a password")

        user = self.model(username=username, full_name=full_name)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username: str, password: str) -> User:
        if password is None:
            raise TypeError("Superuser must have a password")

        user = self.create_user(username, password)
        user.is_admin = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser):
    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["password"]

    username = models.CharField(max_length=120, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self) -> str:
        return self.username

    def has_perm(self, *args: Any, **kwargs: dict[str, Any]) -> bool:
        return self.is_admin

    def has_module_perms(self, *args: Any, **kwargs: dict[str, Any]) -> bool:
        return self.is_admin
