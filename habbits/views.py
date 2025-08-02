from rest_framework.permissions import IsAuthenticated

from .models import Habbit
from .paginators import StandardResultsSetPagination

from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from .serializers import HabbitSerializer

from users.permissions import IsOwner


class PublicHabbitListAPIView(ListAPIView):
    queryset = Habbit.objects.filter(is_public=True)

class HabbitViewSet(ModelViewSet):
    queryset = Habbit.objects.all()
    pagination_class = StandardResultsSetPagination
    serializer_class = HabbitSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        self.permission_classes = [IsAuthenticated, IsOwner]