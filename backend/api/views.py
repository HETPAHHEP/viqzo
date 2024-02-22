from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework import generics, mixins, status, viewsets
from rest_framework.decorators import action as new_action, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView

from links.models import AliasShortLink, ShortLink, UserGroup

from .permissons import IsOwnerAdminOrReadOnly, IsOwnerOrAdmin
from .serializers import (AliasLinkShowSerializer, LinkEditSerializer,
                          LinkWriteSerializer, ShortLinkShowSerializer,
                          UserGroupReadSerializer, UserGroupWriteSerializer)
from .paginators import LinksPagination


class BaseShortLinkView(APIView):
    """Базовый View для короткой ссылки"""
    serializer_short = ShortLinkShowSerializer
    serializer_alias = AliasLinkShowSerializer

    @staticmethod
    def get_serializer(instance):
        """Для коротких и пользовательских ссылок"""
        if isinstance(instance, ShortLink):
            return ShortLinkShowSerializer
        return AliasLinkShowSerializer


class CreateShortLinkOrGetLinksView(BaseShortLinkView, GenericAPIView):
    """View для создания (или получения) короткой ссылки"""
    serializer_create = LinkWriteSerializer
    pagination_class = LinksPagination

    @permission_classes([IsAuthenticated])
    def get(self, request) -> Response:
        """Получение ссылок пользователя"""
        user = request.user
        links = []

        short_links = ShortLink.objects.filter(owner=user).order_by('-created_at')
        alias_links = AliasShortLink.objects.filter(owner=user).order_by('-created_at')

        links.extend(self.serializer_short(short_links, many=True).data)
        links.extend(self.serializer_alias(alias_links, many=True).data)

        return Response(
            data=links,
            status=status.HTTP_200_OK
        )

    def post(self, request) -> Response:
        """Создание или получения уже созданных коротких ссылок"""

        serializer = self.serializer_create(
            data=request.data, context={'user': request.user}
        )
        if serializer.is_valid(raise_exception=True):
            instance, created = serializer.save()
            serializer = self.get_serializer(instance)

            if created:
                return Response(
                    serializer(instance=instance).data,
                    status=status.HTTP_201_CREATED
                )

            # ссылка уже существует
            return Response(
                serializer(instance=instance).data,
                status=status.HTTP_200_OK
            )
        # ошибки при создании
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LinkActionsView(BaseShortLinkView):
    """View для получения или изменения статуса короткой ссылки"""
    serializer_edit = LinkEditSerializer
    permission_classes = [IsOwnerAdminOrReadOnly]

    def get(self, request, short_url) -> Response:
        """Получить ссылку"""
        short_link = ShortLink.objects.filter(short_url=short_url)

        if not short_link:
            short_link = AliasShortLink.objects.filter(alias=short_url)

            if not short_link:
                return Response(
                    {"error": _("Ссылка не найдена.")},
                    status=status.HTTP_404_NOT_FOUND
                )

        short_link = short_link.first()
        short_link.clicks_count += 1
        short_link.save()

        serializer = self.get_serializer(short_link)

        return Response(
            serializer(instance=short_link).data,
            status=status.HTTP_200_OK
        )

    def patch(self, request, short_url) -> Response:
        """Изменение статуса ссылки"""

        short_link = ShortLink.objects.filter(short_url=short_url)

        if not short_link:
            short_link = AliasShortLink.objects.filter(alias=short_url)

            if not short_link:
                return Response(
                    {"error": _("Ссылка не найдена.")},
                    status=status.HTTP_404_NOT_FOUND
                )
        short_link = short_link.first()

        if short_link.owner != request.user:
            return Response(
                {"error": _("Вы не являетесь владельцем ссылки.")},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.serializer_edit(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid(raise_exception=True):
            serializer_response = self.get_serializer(short_link)

            status_active = serializer.data.get('is_active')

            if status_active == short_link.is_active:
                return Response(
                    status=status.HTTP_204_NO_CONTENT
                )

            short_link.is_active = status_active

            group = serializer.data.get('group')

            if short_link.group != group:
                short_link.group = group

            short_link.save()

            return Response(
                serializer_response(instance=short_link).data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, short_url) -> Response:
        """Удаление ссылки"""
        short_link = ShortLink.objects.filter(short_url=short_url)

        if not short_link:
            short_link = AliasShortLink.objects.filter(alias=short_url)

            if not short_link:
                return Response(
                    {"error": _("Ссылка не найдена.")},
                    status=status.HTTP_404_NOT_FOUND
                )
        short_link = short_link.first()

        if short_link.owner == request.user:
            short_link.delete()

            return Response(
                status=status.HTTP_204_NO_CONTENT
            )

        return Response(
            {"error": _("Вы не являетесь владельцем ссылки.")},
            status=status.HTTP_400_BAD_REQUEST
        )


class UserGroupLinkViewSet(viewsets.ModelViewSet):
    """Viewset для получения/добавления/удаления ссылки из группы,
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
