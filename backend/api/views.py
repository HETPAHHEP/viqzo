from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework import generics, mixins, status, viewsets
from rest_framework.decorators import action as new_action
from rest_framework.decorators import permission_classes
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from links.models import ShortLink, UserGroup

from .paginators import LinksPagination
from .permissons import IsOwnerAdminOrReadOnly, IsOwnerOrAdmin
from .serializers import (ShortLinkEditSerializer, ShortLinkReadSerializer,
                          ShortLinkWriteSerializer, UserGroupReadSerializer,
                          UserGroupWriteSerializer)


class ShortLinkViewSet(viewsets.ModelViewSet):
    """ViewSet для действий с короткой ссылкой
    (создание, изменение, удаление, получение всех ссылок и оригинальной ссылки)
    """
    lookup_field = 'short'

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
        if self.action in ('list', 'update', 'partial_update', 'destroy'):
            if not self.request.user.is_staff:
                return ShortLink.objects.filter(owner=self.request.user)
        return ShortLink.objects.all()

    def get_serializer_class(self):
        """Выдача сериализатор к действию"""
        if self.action == 'create':
            return ShortLinkWriteSerializer
        if self.action in ('update', 'partial_update'):
            return ShortLinkEditSerializer
        if self.action in ('list', 'retrieve'):
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

    def perform_destroy(self, instance):
        instance.delete()
