from typing import OrderedDict

from django.db.transaction import atomic
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from core.enums import Limits
from links import validators
from links.models import ShortLink, UserGroup

from .services.short_links import validate_alias, validate_group_for_link


class UserGroupReadSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра группы"""
    owner = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = UserGroup
        fields = [
            'id', 'name', 'owner',
            'color', 'created_at',
        ]


class UserGroupWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для создания/изменения информации о группы"""

    class Meta:
        model = UserGroup
        fields = [
            'name',
        ]
        write_only = True

    def to_representation(self, instance):
        return UserGroupReadSerializer(instance).data


class ShortLinkReadSerializer(serializers.ModelSerializer):
    """Сериализатор для показа ссылок"""
    owner = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    group = UserGroupReadSerializer(read_only=True)

    class Meta:
        model = ShortLink
        fields = [
            'id', 'original_link',
            'short', 'owner', 'clicks_count',
            'last_clicked_at', 'is_active', 'created_at',
            'group'
        ]
        read_only = True


class ShortLinkWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для записи ссылок"""
    alias = serializers.CharField(
        source='short',
        max_length=Limits.MAX_LEN_LINK_SHORT_CODE,
        min_length=Limits.MIN_LEN_LINK_SHORT_CODE,
        validators=[validators.AliasCodeValidator],
        required=False
    )

    def validate(self, data: OrderedDict) -> OrderedDict:
        """Валидация данных"""
        user = self.context.get('request').user

        data_valid_alias = validate_alias(data)
        return validate_group_for_link(data_valid_alias, user)

    def to_representation(self, instance):
        return ShortLinkReadSerializer(instance).data

    class Meta:
        model = ShortLink
        fields = [
            'original_link', 'alias', 'group'
        ]
        write_only = True


class ShortLinkEditSerializer(serializers.Serializer):
    """Сериализатор для активации/деактивации"""
    is_active = serializers.BooleanField(
        help_text=_('Активна ли ссылка?')
    )
    group = serializers.PrimaryKeyRelatedField(
        required=False, queryset=UserGroup.objects.all()
    )

    def validate(self, attrs):
        user = self.context.get('request').user
        return validate_group_for_link(attrs, user)
