from rest_framework.routers import DefaultRouter

from general.views import MediaFileViewSet, ResponseViewSet

router = DefaultRouter()

router.register(r'^media-files', MediaFileViewSet)

router.register(r'^info/response', ResponseViewSet)