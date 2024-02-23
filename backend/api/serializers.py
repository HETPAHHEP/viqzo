from typing import OrderedDict

from django.db.transaction import atomic
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from core.enums import Limits
from links import validators
from links.models import AliasShortLink, ShortLink, User, UserGroup

from .services.short_links import (create_link, validate_alias,
                                   validate_group_for_link)


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

    def to_representation(self, instance):
        return UserGroupReadSerializer(instance).data


class ShortLinkReadSerializer(serializers.ModelSerializer):
    """Сериализатор для показа ссылок"""
    short = serializers.CharField(source='short_url')
    owner = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    group = UserGroupReadSerializer(read_only=True)

    class Meta:
        model = ShortLink
        fields = [
            'id', 'original_link', 'type',
            'short', 'owner', 'clicks_count',
            'last_clicked_at', 'is_active', 'created_at',
            'group'
        ]


class ShortLinkWriteSerializer(serializers.Serializer):
    """Сериализатор для записи ссылок"""
    original_link = serializers.URLField(
        max_length=Limits.MAX_LEN_ORIGINAL_LINK
    )
    alias = serializers.CharField(
        max_length=Limits.MAX_LEN_ALIAS_CODE,
        min_length=Limits.MIN_LEN_ALIAS_CODE,
        validators=[validators.AliasShortURLValidator],
        required=False
    )
    group = serializers.PrimaryKeyRelatedField(
        required=False, queryset=UserGroup.objects.all()
    )

    def validate(self, data: OrderedDict) -> OrderedDict:
        """Валидация данных"""
        user = self.context.get('user')

        data_valid_alias = validate_alias(data)
        return validate_group_for_link(data_valid_alias, user)

    @atomic
    def create(self, valid_data) -> tuple[ShortLink, bool]:
        """Создание сокращенной ссылки для оригинальной"""
        user = self.context.get('user')

        if user.is_authenticated:
            return create_link(valid_data, user)
        return create_link(valid_data)

    def to_representation(self, instance_and_status):
        instance, created_status = instance_and_status
        return UserGroupReadSerializer(instance).data


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


# class AliasLinkShowSerializer(serializers.ModelSerializer):
#     """Сериализатор для показа ссылок"""
#     short = serializers.CharField(source='alias')
#     type = serializers.CharField(default='alias', read_only=True)
#     owner = serializers.SlugRelatedField(
#         slug_field='username',
#         read_only=True
#     )
#     group = UserGroupReadSerializer(read_only=True)
#
#     class Meta:
#         model = AliasShortLink
#         fields = [
#             'id', 'original_link', 'type',
#             'short', 'owner', 'clicks_count',
#             'last_clicked_at', 'is_active', 'created_at',
#             'group',
#         ]
