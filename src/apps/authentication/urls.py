from django.urls import re_path as path

from apps.authentication.views import AuthenticationAPIView, RegistrationAPIView

urlpatterns = [
    path(r"auth/$", AuthenticationAPIView.as_view(), name="user-login"),
    path(r"auth/sign-up/$", RegistrationAPIView.as_view(), name="user-sign-up"),
]
