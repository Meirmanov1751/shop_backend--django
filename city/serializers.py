from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import Serializer, ModelSerializer
from .models import City


class CitySerializer(ModelSerializer):
  class Meta:
    model = City
    fields = '__all__'

