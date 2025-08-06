from django.urls import path, include

from .apps import HabbitsConfig
from .views import PublicHabbitListAPIView, HabbitViewSet

from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(r"", HabbitViewSet, basename="habbit")

app_name = HabbitsConfig.name

urlpatterns = [
    path("public/", PublicHabbitListAPIView.as_view(), name="publichabbits"),
    path("", include(router.urls)),
]
