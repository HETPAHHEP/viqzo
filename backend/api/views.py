from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from links.models import ShortLink, UserGroup

from .filters import LinkFilter
from .paginators import GroupPagination, LinkPagination
from .permissons import IsOwnerOrAdmin
from .serializers import (ShortLinkEditSerializer, ShortLinkReadSerializer,
                          ShortLinkWriteSerializer, UserGroupReadSerializer,
                          UserGroupWriteSerializer)


class ShortLinkViewSet(viewsets.ModelViewSet):
    """ViewSet для действий с короткой ссылкой
    (создание, изменение, удаление,
    получение всех ссылок и оригинальной ссылки)
    """
    lookup_field = 'short'
    pagination_class = LinkPagination
    filter_backends = [
        DjangoFilterBackend, SearchFilter, OrderingFilter
    ]
    filterset_class = LinkFilter
    ordering_fields = [
        'group', 'created_at', 'original_link',
        'clicks_count', 'last_clicked_at',
    ]
    search_fields = ['original_link']

    def get_permissions(self):
        """Выдача разрешения в зависимости от действия"""
        permissions = []  # noqa

        if self.action == 'list':
            permissions = [IsAuthenticated]
        if self.action in ('update', 'partial_update', 'destroy'):
            permissions = [IsOwnerOrAdmin]
        return [permission() for permission in permissions]

    def get_queryset(self):
        """Выдача queryset к действию"""
        queryset = ShortLink.objects.all()

        if self.action in ('list', 'update', 'partial_update', 'destroy'):
            if not self.request.user.is_staff:
                queryset = queryset.filter(owner=self.request.user)

        return queryset

    def get_serializer_class(self):
        """Выдача сериализатор к действию"""
        if self.action == 'create':
            return ShortLinkWriteSerializer
        if self.action in ('update', 'partial_update'):
            return ShortLinkEditSerializer
        return ShortLinkReadSerializer

    def retrieve(self, request, *args, **kwargs):
        link = self.get_object()

        link.clicks_count += 1
        link.save()

        serializer = self.get_serializer(link)
        return Response(serializer.data)

    def perform_create(self, serializer):
        user = self.request.user

        if user.is_authenticated:
            serializer.save(owner=user)
        serializer.save()


class UserGroupLinkViewSet(viewsets.ModelViewSet):
    """ViewSet для получения/добавления/удаления ссылки из группы,
    а также изменения информации о группе.
    """
    pagination_class = GroupPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    actions_without_create = [
        'list', 'retrieve', 'update',
        'partial_update', 'destroy'
    ]

    def get_permissions(self):
        """Выдача разрешения в зависимости от действия"""
        permissions = []  # noqa

        if self.action == 'create':
            permissions = [IsAuthenticated]
        if self.action in self.actions_without_create:
            permissions = [IsOwnerOrAdmin]
        return [permission() for permission in permissions]

    def get_queryset(self):
        if not self.request.user.is_staff:
            return UserGroup.objects.filter(owner=self.request.user)
        return UserGroup.objects.all()

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return UserGroupWriteSerializer
        if self.action in ('list', 'retrieve'):
            return UserGroupReadSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
