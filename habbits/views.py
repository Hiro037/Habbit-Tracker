from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Habbit
from .paginators import StandardResultsSetPagination
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from .serializers import HabbitSerializer
from users.permissions import IsOwner
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status


@method_decorator(cache_page(60 * 5), name="dispatch")
class PublicHabbitListAPIView(ListAPIView):
    queryset = Habbit.objects.filter(is_public=True).order_by('id')
    serializer_class = HabbitSerializer
    permission_classes = [AllowAny]

@method_decorator(cache_page(60 * 5), name="dispatch")
class HabbitViewSet(ModelViewSet):
    queryset = Habbit.objects.all().order_by('id')
    pagination_class = StandardResultsSetPagination
    serializer_class = HabbitSerializer

    def get_queryset(self):
        return Habbit.objects.filter(user=self.request.user).order_by('id')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action == 'retrieve':
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsOwner()]

    def retrieve(self, request, *args, **kwargs):
        # Получаем объект (не только среди объектов текущего пользователя!)
        obj = get_object_or_404(Habbit, pk=kwargs['pk'])

        if obj.is_public:
            # Публичный — любой авторизованный может получить доступ
            return Response(self.get_serializer(obj).data)
        else:
            # Не публичный — проверяем, является ли пользователь владельцем
            if obj.user != request.user:
                return Response({'detail': 'Недостаточно прав.'}, status=status.HTTP_403_FORBIDDEN)
            return Response(self.get_serializer(obj).data)
