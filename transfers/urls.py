from rest_framework.routers import DefaultRouter

from .views import ClubViewSet, PlayerViewSet, TransferViewSet

router = DefaultRouter()
router.register(r"players", PlayerViewSet)
router.register(r"clubs", ClubViewSet)
router.register(r"transfers", TransferViewSet)

urlpatterns = router.urls
