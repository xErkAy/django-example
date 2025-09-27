from django.urls import path

from apps.testapp.api import views

urlpatterns = [
    path(r"api/test/", views.TestAPIView.as_view(), name="test_api_view"),
    path(r"api/upload/", views.UploadAPIView.as_view(), name="upload_api_view"),
    path(r"api/download/", views.DownloadAPIView.as_view()),
]
