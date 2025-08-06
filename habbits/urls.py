from django.urls import path, include

from .apps import HabbitsConfig
from .views import PublicHabbitListAPIView, HabbitViewSet

from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(r"", HabbitViewSet, basename="habbit")

app_name = HabbitsConfig.name

urlpatterns = [
    path("", include(router.urls)),
    path("public/", PublicHabbitListAPIView.as_view(), name="publichabbits"),
]
