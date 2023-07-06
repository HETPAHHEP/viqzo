from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from core.enums import Limits
from links.models import ShortLink, AliasShortLink
from links import validators

from .services.url_short_logic import LinkHash


class ShortLinkShowSerializer(serializers.ModelSerializer):
    """Сериализатор для показа ссылок"""

    class Meta:
        model = ShortLink
        fields = [
            'original_link', 'short_url', 'clicks_count',
            'last_clicked_at', 'is_active', 'created_at'
        ]


class AliasLinkShowSerializer(serializers.ModelSerializer):
    """Сериализатор для показа ссылок"""
    short_url = serializers.CharField(source='alias')

    class Meta:
        model = ShortLink
        fields = [
            'original_link', 'short_url', 'clicks_count',
            'last_clicked_at', 'is_active', 'created_at'
        ]


class LinkWriteSerializer(serializers.Serializer):
    """Сериализатор для записи ссылок"""
    original_link = serializers.URLField(
        max_length=Limits.MAX_LEN_ORIGINAL_LINK.value
    )
    alias = serializers.CharField(
        max_length=Limits.MAX_LEN_ALIAS_CODE.value,
        min_length=Limits.MIN_LEN_ALIAS_CODE.value,
        validators=[validators.AliasShortURLValidator],
        required=False
    )

    def validate(self, attrs):
        alias = attrs.get('alias')

        if alias:

            if AliasShortLink.objects.filter(alias=alias).exists():
                raise serializers.ValidationError({
                    'alias_error': _('Данный код для ссылки уже занят.')
                })

        return attrs

    def create(self, validated_data) -> tuple[ShortLink, bool]:
        """Создание сокращенной ссылки для оригинальной"""
        original_link = validated_data.get('original_link')
        alias = validated_data.get('alias')

        if alias:
            url = AliasShortLink.objects.create(
                original_link=original_link,
                alias=alias
            )
            created = True

        else:
            url, created = ShortLink.objects.get_or_create(
                original_link=original_link
            )

        if created and not alias:
            while not url.short_url:
                # проверяем, не занят ли короткий код и присваиваем его ссылке
                short_code = LinkHash().get_short_code()

                if not ShortLink.objects.filter(short_url=short_code).exists():
                    url.short_url = short_code
                    url.save()

        return url, created
