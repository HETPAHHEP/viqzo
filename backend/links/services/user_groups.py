from random import choice

from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework.validators import ValidationError

from core.enums import Limits

from .colors import colors_palette


def check_group_constraints(model, user):
    """Проверка ограничений группы"""
    groups_count = model.objects.filter(owner=user).count()

    if groups_count >= Limits.MAX_GROUPS_AMOUNT:
        raise ValidationError({
            'groups_error': _(
                'Превышено максимальное количество групп для пользователя.'
            )
        })


def set_color_for_group(model, instance) -> str:
    """Добавление цвета к группе"""

    # Получаем список цветов, которые уже используются
    used_colors = model.objects.exclude(
        pk=instance.pk).values_list('color', flat=True)

    # Получаем список доступных цветов, которые еще не использованы
    available_colors = [
        color.color_hex for color in colors_palette
        if color.color_hex not in used_colors
    ]

    if not available_colors:
        raise ValidationError({
            'color_error': _('Нет доступных цветов для группы')
        })

    return choice(available_colors)


def full_clean_check_validation_name(group):
    """Проверка ограничений имени у групп"""
    try:
        group.full_clean()  # Выполняем проверку перед сохранением
    except DjangoValidationError as e:
        if 'name' in e.error_dict:
            raise ValidationError({
                'name_error': e.error_dict['name']
            })

        if '__all__' in e.error_dict:
            raise ValidationError({
                'name_error': _('Группа с таким именем уже существует.'),
                'original_error': e.error_dict,
            })
            # Если другие ошибки, просто передаем исключение дальше
        raise
