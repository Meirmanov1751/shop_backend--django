from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from .serializers import OrderSerializer, OrderItemSerializer
from .models import Order, OrderItem


class OrderViewSet(mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin,
                  mixins.DestroyModelMixin, GenericViewSet):
  serializer_class = OrderSerializer
  queryset = Order.objects.all()


class OrderItemViewSet(mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin,
                  mixins.DestroyModelMixin, GenericViewSet):
  serializer_class = OrderItemSerializer
  queryset = OrderItem.objects.all()
