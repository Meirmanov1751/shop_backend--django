from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from general.models import MediaFile, Version, ResponseAboutApp
from general.serializers import MediaFileSerializer, VersionSerializer, ResponseSerializer


class MediaFileViewSet(ModelViewSet):
    queryset = MediaFile.objects.all()
    serializer_class = MediaFileSerializer


class ResponseViewSet(ModelViewSet):
    queryset = ResponseAboutApp.objects.all()
    serializer_class = ResponseSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

#TODO remove this later
@api_view(['GET'])
@permission_classes([AllowAny])
def app_version(request):
    version = Version.objects.filter(type=Version.TYPES.FLUTTER)
    if version.exists():
        version = version.first()
        serializer = VersionSerializer(instance=version)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def ios_version(request):
    version = Version.objects.filter(type=Version.TYPES.IOS)
    if version.exists():
        version = version.first()
        serializer = VersionSerializer(instance=version)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def android_version(request):
    version = Version.objects.filter(type=Version.TYPES.ANDROID)
    if version.exists():
        version = version.first()
        serializer = VersionSerializer(instance=version)
        return Response(serializer.data)