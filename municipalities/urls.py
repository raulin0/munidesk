from rest_framework.routers import DefaultRouter

from .views import (
    MunicipalityViewSet,
    PositionViewSet,
    PublicBodyViewSet,
    PublicOfficialViewSet,
)

router = DefaultRouter()
router.register("municipalities", MunicipalityViewSet)
router.register("public-bodies", PublicBodyViewSet)
router.register("positions", PositionViewSet)
router.register("public-officials", PublicOfficialViewSet)

urlpatterns = router.urls
