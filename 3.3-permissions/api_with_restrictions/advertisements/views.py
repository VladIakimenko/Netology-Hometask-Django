from django.contrib.auth.models import AnonymousUser
from django.db.models import Q
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404

from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement, Favorite
from advertisements.serializers import AdvertisementSerializer, FavoriteSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    serializer_class = AdvertisementSerializer
    filterset_fields = ['creator', 'created_at', 'status']
    filterset_class = AdvertisementFilter

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            queryset = Advertisement.objects.all()
        elif isinstance(user, AnonymousUser):
            queryset = Advertisement.objects.filter(draft=False)
        else:
            queryset = Advertisement.objects.filter(
                Q(draft=False) |
                Q(draft=True, creator=user)
            )
        return queryset

    def get_permissions(self):
        """Получение прав для действий."""
        if self.request.user.is_staff or self.action not in [
            'update',
            'partial_update',
            'destroy',
            'create'
        ]:
            return []
        else:
            if self.action != 'create':
                obj = get_object_or_404(Advertisement, id=self.kwargs['pk'])
                if self.request.user != obj.creator:
                    raise PermissionDenied("User is not the owner of the advertisement or not authenticated")
            return [IsAuthenticated()]


class FavoriteViewSet(ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        user = self.request.user
        if self.request.user.is_staff:
            return Favorite.objects.all()
        else:
            return Favorite.objects.filter(user=user)

    def get_permissions(self):
        """Получение прав для действий."""
        return [IsAuthenticated()]
