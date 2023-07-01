from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import LinkReadSerializer, LinkWriteSerializer


class ShortLinkView(APIView):
    """View для взаимодействия со ссылками"""
    def post(self, request) -> Response:
        serializer = LinkWriteSerializer(data=request.data)
        if serializer.is_valid():
            instance, created = serializer.save()
            if created:
                return Response(
                    LinkReadSerializer(instance=instance).data,
                    status=status.HTTP_201_CREATED
                )
            # ссылка уже существует
            return Response(
                LinkReadSerializer(instance=instance).data,
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
