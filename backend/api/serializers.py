from collections import OrderedDict

from rest_framework import status, serializers
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _

from core.enums import Limits
from links.models import ShortLink, UserGroup

from .validators import AliasCodeValidator
from .services.links_file import check_request_fields, check_user_groups_amount
from .services.short_links import validate_alias, validate_group_for_link


class UserGroupReadSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра группы"""

    owner = serializers.SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = UserGroup
        fields = [
            "id",
            "name",
            "owner",
            "color",
            "created_at",
        ]


class UserGroupWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для создания/изменения информации о группы"""

    class Meta:
        model = UserGroup
        fields = [
            "name",
        ]
        write_only = True

    def to_representation(self, instance):
        return UserGroupReadSerializer(instance).data


class ShortLinkReadSerializer(serializers.ModelSerializer):
    """Сериализатор для показа ссылок"""

    owner = serializers.SlugRelatedField(slug_field="username", read_only=True)
    group = UserGroupReadSerializer(read_only=True)

    class Meta:
        model = ShortLink
        fields = [
            "id",
            "original_link",
            "short",
            "owner",
            "clicks_count",
            "last_clicked_at",
            "is_active",
            "created_at",
            "group",
        ]
        read_only = True


class ShortLinkWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для записи ссылок"""

    alias = serializers.CharField(
        source="short",
        label="Алиас",
        help_text="Короткий код ссылки",
        max_length=Limits.MAX_LEN_LINK_SHORT_CODE,
        min_length=Limits.MIN_LEN_LINK_SHORT_CODE,
        validators=[AliasCodeValidator()],
        required=False,
    )

    def validate(self, data: OrderedDict) -> OrderedDict:
        """Валидация данных"""
        user = self.context.get("request").user

        data_valid_alias = validate_alias(data)
        return validate_group_for_link(data_valid_alias, user)

    def to_representation(self, instance):
        return ShortLinkReadSerializer(instance).data

    class Meta:
        model = ShortLink
        fields = ["original_link", "alias", "group"]
        write_only = True


class ShortLinkEditSerializer(serializers.Serializer):
    """Сериализатор для активации/деактивации"""

    is_active = serializers.BooleanField(
        required=False, help_text=_("Активна ли ссылка?")
    )
    group = serializers.PrimaryKeyRelatedField(
        required=False, queryset=UserGroup.objects.all()
    )

    def validate(self, attrs):
        """Проверка введённых данных"""
        user = self.context.get("request").user
        return validate_group_for_link(attrs, user)

    def update(self, instance, validated_data):
        """Изменение группы и статуса ссылки"""
        active_status = validated_data.pop("is_active", None)
        group = validated_data.pop("group", None)

        if (
            isinstance(active_status, bool)
            and instance.is_active != active_status
        ):
            instance.is_active = active_status

        if group and instance.group != group:
            instance.group = group

        instance.save()

        return instance

    def to_representation(self, instance):
        return ShortLinkReadSerializer(instance).data


class LinksExportWriteSerializer(serializers.Serializer):
    """Сериализатор для добавления пользовательских ссылок из файла"""

    group_name = serializers.CharField(
        required=False,
        allow_blank=False,
        max_length=Limits.MAX_LEN_GROUP_NAME,
        help_text="Имя новой группы для ссылок из файла",
    )
    group_id = serializers.PrimaryKeyRelatedField(
        required=False,
        many=False,
        allow_empty=False,
        queryset=UserGroup.objects.all(),
        help_text="ID существующей группы",
    )
    file = serializers.FileField(
        required=True,
        allow_empty_file=False,
        allow_null=False,
        max_length=int(Limits.MAX_LINKS_GROUP_AMOUNT * 1024 * 2),
        validators=[
            FileExtensionValidator(
                allowed_extensions=["csv", "json"],
                code=status.HTTP_400_BAD_REQUEST,
                message=_(
                    "Неправильное расширение файла. "
                    "Разрешены CSV и JSON файлы"
                ),
            )
        ],
        help_text=_(
            "Файл с ссылками и их опциональными "
            "алиасами в формате CSV или JSON"
        ),
    )

    class Meta:
        write_only = True

    def validate(self, attrs):
        """Проверка ограничений и валидация"""
        user = self.context.get("request").user
        check_user_groups_amount(user)
        check_request_fields(attrs)

        return attrs
