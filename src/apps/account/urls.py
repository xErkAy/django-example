from django.urls import re_path as path

from src.apps.account.views import (
    AuthenticationAPIView,
    RegistrationAPIView,
    ProfileAPIView
)

urlpatterns = [
    path(r'auth/$', AuthenticationAPIView.as_view(), name='user-login'),
    path(r'auth/sign-up/$', RegistrationAPIView.as_view(), name='user-sign-up'),
    path(r'profile/$', ProfileAPIView.as_view(), name='profile'),
]