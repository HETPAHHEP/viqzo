from rest_framework import serializers

from core.enums import Limits
from links.models import ShortLink

from .services.url_short_logic import LinkHash


class LinkReadSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения ссылок"""

    class Meta:
        model = ShortLink
        fields = ['original_link', 'short_url', 'created_at']


class LinkWriteSerializer(serializers.Serializer):
    """Сериализатор для записи ссылок"""
    original_link = serializers.URLField(
        max_length=Limits.MAX_LEN_ORIGINAL_LINK
    )

    def create(self, validated_data) -> tuple[ShortLink, bool]:
        """Создание сокращенной ссылки для оригинальной"""
        original_link = validated_data.get('original_link')
        url, created = ShortLink.objects.get_or_create(
            original_link=original_link
        )

        if created:
            while not url.short_url:
                # проверяем, не занят ли короткий код и присваиваем его ссылке
                short_code = LinkHash().get_short_code()

                if not ShortLink.objects.filter(short_url=short_code).exists():
                    url.short_url = short_code
                    url.save()

        return url, created
