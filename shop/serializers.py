from rest_framework.serializers import ModelSerializer
from .models import Shop, ShopItem, ShopSchedule, ShopItemImage, ShopItemDetail, ShopWorkTime


class ShopSerializer(ModelSerializer):
  class Meta:
    model = Shop
    fields = '__all__'


class ShopItemSerializer(ModelSerializer):
  class Meta:
    model = ShopItem
    fields = '__all__'


# class ShopOrderSerializer(ModelSerializer):
  # class Meta:
  #   model = ShopOrder
  #   fields = '__all__'


class ShopScheduleSerializer(ModelSerializer):
  class Meta:
    model = ShopSchedule
    fields = '__all__'


# class ShopOrderItemSerializer(ModelSerializer):
#   class Meta:
#     model = ShopOrderItem
#     fields = '__all__'


class ShopItemImageSerializer(ModelSerializer):
  class Meta:
    model = ShopItemImage
    fields = '__all__'


class ShopItemDetailSerializer(ModelSerializer):
  class Meta:
    model = ShopItemDetail
    fields = '__all__'


class ShopWorkTimeSerializer(ModelSerializer):
  class Meta:
    model = ShopWorkTime
    fields = '__all__'
