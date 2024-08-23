from random import choice

from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import APIException
from rest_framework.validators import ValidationError

from core.enums import Limits


def check_group_constraints(model, user):
    """Проверка ограничений группы"""
    groups_count = model.objects.filter(owner=user).count()

    if groups_count >= Limits.MAX_GROUPS_AMOUNT:
        raise ValidationError(
            {
                "groups_error": _(
                    "Превышено максимальное количество групп для пользователя."
                )
            }
        )


def set_color_for_group(group_model, instance, color_group) -> str:
    """Добавление цвета к группе"""

    # Получаем список цветов, которые уже используются
    used_colors = group_model.objects.exclude(pk=instance.pk).values_list(
        "color", flat=True
    )

    if not color_group.objects.exists():
        raise APIException(
            {
                "color_error": _(
                    "В базе данных отсутствуют какие либо записи "
                    "цветов для группы"
                )
            }
        )

    colors_palette = list(color_group.objects.exclude(pk__in=used_colors))

    if not colors_palette:
        raise ValidationError(
            {"color_error": _("Нет доступных цветов для группы")}
        )

    return choice(colors_palette)


def full_clean_check_validation_name(group):
    """Проверка ограничений имени у групп"""
    try:
        group.full_clean()  # Выполняем проверку перед сохранением
    except DjangoValidationError as e:
        if "name" in e.error_dict:
            raise ValidationError({"name_error": e.error_dict["name"]}) from e

        if "__all__" in e.error_dict:
            raise ValidationError(
                {
                    "name_error": _("Группа с таким именем уже существует."),
                    "original_error": e.error_dict,
                }
            ) from e
            # Если другие ошибки, просто передаем исключение дальше
        raise
