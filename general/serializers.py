from rest_framework.serializers import ModelSerializer

from .models import MediaFile, ResponseAboutApp, Version


class MediaFileSerializer(ModelSerializer):
    class Meta:
        model = MediaFile
        fields = '__all__'



class ResponseSerializer(ModelSerializer):
    class Meta:
        model = ResponseAboutApp
        fields = '__all__'


class VersionSerializer(ModelSerializer):
    class Meta:
        model = Version
        fields = '__all__'
