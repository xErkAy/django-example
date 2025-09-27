from django.urls import re_path as path

from apps.account.api.views import ProfileAPIView

urlpatterns = [
    path(r"profile/$", ProfileAPIView.as_view(), name="profile"),
]
