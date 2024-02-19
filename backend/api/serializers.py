from typing import OrderedDict

from django.db.transaction import atomic
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from core.enums import Limits
from links import validators
from links.models import (AliasShortLink, ShortLink, User, UserGroup,
                          UserGroupLink)

from .services.short_links import create_link, validate_alias
from .services.usergroup import validate_links_for_group


class ShortLinkShowSerializer(serializers.ModelSerializer):
    """Сериализатор для показа ссылок"""
    short = serializers.CharField(source='short_url')
    type = serializers.CharField(default='short')
    owner = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = ShortLink
        fields = [
            'id', 'original_link', 'type',
            'short', 'owner', 'clicks_count',
            'last_clicked_at', 'is_active', 'created_at',
        ]


class AliasLinkShowSerializer(serializers.ModelSerializer):
    """Сериализатор для показа ссылок"""
    short = serializers.CharField(source='alias')
    type = serializers.CharField(default='alias')
    owner = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = AliasShortLink
        fields = [
            'id', 'original_link', 'type',
            'short', 'owner', 'clicks_count',
            'last_clicked_at', 'is_active', 'created_at',
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


class UserGroupReadSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра группы"""
    owner = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = UserGroup
        fields = [
            'id', 'name', 'owner',
            'color', 'created_at',
        ]


class UserGroupCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания группы"""

    class Meta:
        model = UserGroup
        fields = [
            'name',
        ]

    def to_representation(self, instance):
        return UserGroupReadSerializer(instance).data


class UserGroupLinkSerializer(serializers.ModelSerializer):
    """Сериализатор для представления данных о связи группы пользователя и ссылки"""

    class Meta:
        model = UserGroupLink
        fields = ['alias_link', 'short_link']


class UserGroupWithLinksReadSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра группы вместе со ссылками"""
    owner = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    links = serializers.SerializerMethodField(
        method_name='get_all_links'
    )

    @staticmethod
    def get_all_links(obj):
        alias_links = []
        short_links = []

        for link in obj.group_links.all():
            if link.alias_link:
                alias_links.append(AliasLinkShowSerializer(link.alias_link).data)
            if link.short_link:
                short_links.append(ShortLinkShowSerializer(link.short_link).data)

        alias_links.extend(short_links)

        return alias_links

    class Meta:
        model = UserGroup
        fields = [
            'id', 'name', 'owner',
            'color', 'created_at', 'links',
        ]


class UserGroupWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для изменения информации о группы"""

    class Meta:
        model = UserGroup
        fields = [
            'name',
        ]

    def to_representation(self, instance):
        return UserGroupReadSerializer(instance).data


class UserGroupLinksWriteSerializer(serializers.Serializer):
    """Сериализатор для добавления/удаления ссылки"""
    short_link = serializers.PrimaryKeyRelatedField(
        required=False, queryset=ShortLink.objects.all()
    )
    alias_link = serializers.PrimaryKeyRelatedField(
        required=False, queryset=AliasShortLink.objects.all()
    )

    def validate(self, attrs):
        user = self.context['request'].user
        return validate_links_for_group(attrs, user)


