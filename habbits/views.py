from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Habbit
from .paginators import StandardResultsSetPagination
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from .serializers import HabbitSerializer
from users.permissions import IsOwner

class PublicHabbitListAPIView(ListAPIView):
    queryset = Habbit.objects.filter(is_public=True).order_by('id')
    serializer_class = HabbitSerializer
    permission_classes = [AllowAny]

class HabbitViewSet(ModelViewSet):
    queryset = Habbit.objects.all().order_by('id')
    pagination_class = StandardResultsSetPagination
    serializer_class = HabbitSerializer

    def get_queryset(self):
        return Habbit.objects.filter(user=self.request.user).order_by('id')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        return [IsAuthenticated(), IsOwner()]
