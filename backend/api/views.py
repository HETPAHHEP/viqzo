from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin

from .serializers import LinkReadSerializer, LinkWriteSerializer
from .services.url_short_logic import LinkHash

from links.models import ShortLink


class LinkViewSet(CreateModelMixin, RetrieveModelMixin, GenericViewSet):
    """Viewset для взаимодействия со ссылками"""
    queryset = ShortLink.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return LinkWriteSerializer
        return LinkReadSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        shortened_link_code = LinkHash().to_base_62(instance.id)
        instance.short_url = shortened_link_code
        instance.save()
