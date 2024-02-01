from django.utils.translation import gettext_lazy as _
from rest_framework import generics, mixins, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from links.models import AliasShortLink, ShortLink, UserGroup, UserGroupLink

from .permissons import IsOwnerAdminOrReadOnly
from .serializers import (AliasLinkShowSerializer, LinkActivationSerializer,
                          LinkWriteSerializer, ShortLinkShowSerializer,
                          UserGroupCreateSerializer,
                          UserGroupLinkReadSerializer,
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


class CreateGroupViewSet(mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    """Создание/просмотр групп для ссылок"""
    # queryset = UserGroup.objects.all()

    def get_permissions(self):
        """Выдача разрешения в зависимости от действия"""
        permission_classes = []

        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        if self.action == 'list':
            permission_classes = [IsOwnerOrAdmin]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if self.action == 'create':
            return UserGroup.objects.all()
        return UserGroupLink.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return UserGroupCreateSerializer
        return UserGroupReadSerializer


class CreateGroupView(generics.CreateAPIView):
    queryset = UserGroup.objects.all()
    serializer_class = UserGroupCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# class GroupLinkViewActions(APIView):
#     """View для получения/добавления/удаления ссылки из группы"""
#     queryset = UserGroupLinks.objects.all()
#     # serializer_class = UserGroupWriteSerializer
#     permission_classes = [IsOwnerAdminOrReadOnly]

