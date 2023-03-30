from rest_framework.routers import DefaultRouter
from .views import ShopViewSet, ShopWorkTimeViewSet, ShopScheduleViewSet, ShopItemViewSet, ShopItemImageViewSet, \
  ShopItemDetailViewSet

router = DefaultRouter()

router.register(r'^shop', ShopViewSet)
router.register(r'^shopWorkTime', ShopWorkTimeViewSet)
router.register(r'^shopSchedule', ShopScheduleViewSet)
router.register(r'^shopItem', ShopItemViewSet)
router.register(r'^shopItemImage', ShopItemImageViewSet)
router.register(r'^shopItemDetail', ShopItemDetailViewSet)

