from django.conf import settings
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class TestAPIView(APIView):

    def get(self, request, *args, **kwargs):
        return Response({'user': request.user.username})


class UploadAPIView(APIView):
    def post(self, request, *args, **kwargs):
        file = request.data.get('file')
        if file is None:
            return Response(
                {'message': 'No file provided', 'success': False},
                status=status.HTTP_400_BAD_REQUEST
            )

        with open(f'{settings.STATIC_ROOT}{file.__dict__["_name"]}', 'wb') as destination:
            destination.write(file.__dict__['file'].read())

        return Response(status=status.HTTP_200_OK)


class DownloadAPIView(APIView):

    def get(self, request, *args, **kwargs):
        filename = request.query_params.get('name')
        if not filename:
            return Response(
                {'message': 'No filename provided', 'success': False},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            with open(f'{settings.STATIC_ROOT}{filename}', 'rb') as file:
                response = HttpResponse(file)
                response['Content-Disposition'] = f'attachment; filename={filename}'
                return response
        except FileNotFoundError:
            return Response(
                {'message': 'File not found', 'success': False},
                status=status.HTTP_400_BAD_REQUEST
            )