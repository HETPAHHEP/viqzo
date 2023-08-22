from typing import OrderedDict

from django.utils.translation import gettext_lazy as _
from django.db.transaction import atomic
from rest_framework import serializers

from core.enums import Limits
from links import validators
from links.models import AliasShortLink, ShortLink

from .services.short_links import create_link, validate_alias


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
        model = AliasShortLink
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

    def validate(self, data: OrderedDict) -> OrderedDict:
        """Валидация данных"""
        return validate_alias(data)

    @atomic
    def create(self, valid_data) -> tuple[ShortLink | AliasShortLink, bool]:
        """Создание сокращенной ссылки для оригинальной"""
        user = self.context.get('user')

        if user.is_authenticated:
            return create_link(valid_data, user)
        return create_link(valid_data)


class LinkActivationSerializer(serializers.Serializer):
    """Сериализатор для активации/деактивации"""
    is_active = serializers.BooleanField(
        help_text=_('Активна ли ссылка?')
    )
