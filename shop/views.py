from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from .serializers import ShopSerializer, ShopItemSerializer, ShopItemDetailSerializer, ShopItemImageSerializer, \
  ShopScheduleSerializer, ShopWorkTimeSerializer
from .models import Shop, ShopItem, ShopSchedule, ShopItemImage, ShopItemDetail, ShopWorkTime


class ShopViewSet(mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin,
                  mixins.DestroyModelMixin, GenericViewSet):
  serializer_class = ShopSerializer
  queryset = Shop.objects.all()


class ShopItemViewSet(mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin,
                      mixins.CreateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
  serializer_class = ShopItemSerializer
  queryset = ShopItem.objects.all()


class ShopItemDetailViewSet(mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin,
                            mixins.CreateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
  serializer_class = ShopItemDetailSerializer
  queryset = ShopItemDetail.objects.all()


class ShopItemImageViewSet(mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin,
                           mixins.CreateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
  serializer_class = ShopItemImageSerializer
  queryset = ShopItemImage.objects.all()


class ShopScheduleViewSet(mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin,
                          mixins.CreateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
  serializer_class = ShopScheduleSerializer
  queryset = ShopSchedule.objects.all()


class ShopWorkTimeViewSet(mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin,
                          mixins.CreateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
  serializer_class = ShopWorkTimeSerializer
  queryset = ShopWorkTime.objects.all()
