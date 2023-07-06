from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from links.models import ShortLink, AliasShortLink

from .serializers import ShortLinkShowSerializer, LinkWriteSerializer, AliasLinkShowSerializer


class BaseShortLinkView(APIView):
    """Базовый View для короткой ссылки"""

    @staticmethod
    def get_serializer(instance):
        """Для коротких и пользовательских ссылок"""
        if isinstance(instance, ShortLink):
            return ShortLinkShowSerializer
        return AliasLinkShowSerializer


class GetShortLinkView(BaseShortLinkView):
    """View для получения короткой ссылки"""

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


class CreateShortLinkView(BaseShortLinkView):
    """View для создания (или получения) короткой ссылки"""
    serializer_create = LinkWriteSerializer

    def post(self, request) -> Response:
        """Создание или получения уже созданных коротких ссылок"""

        serializer = self.serializer_create(data=request.data)
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
