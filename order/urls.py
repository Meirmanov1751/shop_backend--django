from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, OrderItemViewSet

router = DefaultRouter()

router.register(r'^order', OrderViewSet)
router.register(r'^orderItem', OrderItemViewSet)
