from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from links.models import ShortLink

from .serializers import LinkShowSerializer, LinkWriteSerializer


class ShortLinkView(APIView):
    """View для взаимодействия со ссылками"""

    def get(self, request, short_url) -> Response:
        try:
            short_link = ShortLink.objects.get(short_url=short_url)
            short_link.clicks_count += 1
            short_link.save()

            return Response(
                LinkShowSerializer(instance=short_link).data,
                status=status.HTTP_200_OK
            )
        except ShortLink.DoesNotExist:
            return Response(
                {"error": _("Ссылка не найдена.")},
                status=status.HTTP_404_NOT_FOUND
            )

    def post(self, request) -> Response:
        serializer = LinkWriteSerializer(data=request.data)
        if serializer.is_valid():
            instance, created = serializer.save()
            if created:
                return Response(
                    LinkShowSerializer(instance=instance).data,
                    status=status.HTTP_201_CREATED
                )
            # ссылка уже существует
            return Response(
                LinkShowSerializer(instance=instance).data,
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
