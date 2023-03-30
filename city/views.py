from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from .serializers import CitySerializer
from .models import City


class CityViewSet(mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin,
                  mixins.DestroyModelMixin, GenericViewSet):
  serializer_class = CitySerializer
  queryset = City.objects.all()
