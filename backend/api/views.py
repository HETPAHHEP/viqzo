from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework import generics, mixins, status, viewsets
from rest_framework.decorators import action as new_action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from links.models import AliasShortLink, ShortLink, UserGroup, UserGroupLink

from .permissons import IsOwnerAdminOrReadOnly, IsOwnerOrAdmin
from .serializers import (AliasLinkShowSerializer, LinkActivationSerializer,
                          LinkWriteSerializer, ShortLinkShowSerializer,
                          UserGroupCreateSerializer,
                          UserGroupLinksWriteSerializer,
                          UserGroupReadSerializer,
                          UserGroupWithLinksReadSerializer,
                          UserGroupWriteSerializer)


class BaseShortLinkView(APIView):
    """Базовый View для короткой ссылки"""

    @staticmethod
    def get_serializer(instance):
        """Для коротких и пользовательских ссылок"""
        if isinstance(instance, ShortLink):
            return ShortLinkShowSerializer
        return AliasLinkShowSerializer


class CreateShortLinkView(BaseShortLinkView):
    """View для создания (или получения) короткой ссылки"""
    serializer_create = LinkWriteSerializer

    def post(self, request) -> Response:
        """Создание или получения уже созданных коротких ссылок"""

        serializer = self.serializer_create(
            data=request.data, context={'user': request.user}
        )
        if serializer.is_valid():
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
    """View для получения или изменения короткой ссылки"""
    serializer_edit = LinkActivationSerializer
    permission_classes = [IsOwnerAdminOrReadOnly]

    def get(self, request, short_url) -> Response:
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
        """Изменение ссылки"""

        short_link = ShortLink.objects.filter(short_url=short_url)

        if not short_link:
            short_link = AliasShortLink.objects.filter(alias=short_url)

            if not short_link:
                return Response(
                    {"error": _("Ссылка не найдена.")},
                    status=status.HTTP_404_NOT_FOUND
                )
        short_link = short_link.first()

        serializer = self.serializer_edit(data=request.data)

        if serializer.is_valid():
            serializer_response = self.get_serializer(short_link)

            status_active = serializer.data.get('is_active')

            if status_active == short_link.is_active:
                return Response(
                    status=status.HTTP_204_NO_CONTENT
                )

            short_link.is_active = status_active
            short_link.save()

            return Response(
                serializer_response(instance=short_link).data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
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
        permission_classes = []  # noqa

        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        if self.action in self.actions_without_create:
            permission_classes = [IsOwnerOrAdmin]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if not self.request.user.is_staff:
            return UserGroup.objects.filter(owner=self.request.user)
        return UserGroup.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return UserGroupCreateSerializer
        if self.action in ('list', 'retrieve'):
            return UserGroupWithLinksReadSerializer
        if self.action in ('update', 'partial_update'):
            return UserGroupWriteSerializer

    @new_action(detail=True, methods=['post'], url_path='add-link', url_name='add-link')
    def add_link_to_group(self, request, pk=None):
        """Добавить ссылку в нужную группу"""
        group = self.get_object()
        serializer_links = UserGroupLinksWriteSerializer(
            data=request.data,
            context={
                'request': request
            }
        )

        if serializer_links.is_valid(raise_exception=True):
            alias_link = serializer_links.validated_data.get('alias_link')
            short_link = serializer_links.validated_data.get('short_link')

            if ((
                    UserGroupLink.objects.filter(group=group, alias_link=alias_link).exists()
                    and bool(alias_link)
            )
                    or
                    (
                            UserGroupLink.objects.filter(group=group, short_link=short_link).exists()
                            and bool(short_link)
                    )):
                return Response(
                    {'links_error': 'Ссылка уже существует в этой группе.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            UserGroupLink.objects.create(
                group=group,
                alias_link=alias_link,
                short_link=short_link
            )

            serializer_response = UserGroupWithLinksReadSerializer(
                instance=group
            )

            return Response(
                serializer_response.data,
                status=status.HTTP_201_CREATED
            )

        return Response(serializer_links.errors, status=status.HTTP_400_BAD_REQUEST)

    @new_action(detail=True, methods=['delete'], url_path='remove-link', url_name='remove-link')
    def remove_link_from_group(self, request, pk=None):
        """Удалить ссылку из нужной группы"""
        group = self.get_object()
        serializer_links = UserGroupLinksWriteSerializer(
            data=request.data,
            context={
                'request': request
            }
        )

        if serializer_links.is_valid(raise_exception=True):
            alias_link = serializer_links.validated_data.get('alias_link')
            short_link = serializer_links.validated_data.get('short_link')

            try:
                link_to_delete = None

                if alias_link:
                    link_to_delete = UserGroupLink.objects.get(
                        group=group,
                        alias_link=alias_link
                    )
                if short_link:
                    link_to_delete = UserGroupLink.objects.get(
                        group=group,
                        alias_link=alias_link
                    )

                link_to_delete.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)

            except UserGroupLink.DoesNotExist:
                return Response(
                    {'links_error': 'Cсылка не добавлена в данную группу.'},
                    status=status.HTTP_404_NOT_FOUND
                )

        return Response(serializer_links.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()
