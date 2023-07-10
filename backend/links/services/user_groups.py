from core.enums import Limits
from rest_framework.validators import ValidationError
from .colors import colors_palette
from random import choice
from django.utils.translation import gettext_lazy as _


def check_group_constraints(instance):
    """Проверка ограничений группы"""
    alias_count = instance.alias_links.count()
    short_count = instance.short_links.count()
    groups_count = instance.objects.filter(owner=instance.owner).count()

    if alias_count + short_count >= Limits.MAX_LINKS_GROUP_AMOUNT:
        raise ValidationError({
            'links_error': _(
                'Превышено максимальное количество ссылок для этой группы.'
            )
        })

    if groups_count >= Limits.MAX_GROUPS_AMOUNT:
        raise ValidationError({
            'groups_error': _(
                'Превышено максимальное количество групп для пользователя.'
            )
        })


def set_color_for_group(instance) -> str:
    """Добавление цвета к группе"""

    # Получаем список цветов, которые уже используются
    # used_colors = UserGroup.objects.exclude(pk=instance.pk).values_list('color', flat=True)
    used_colors = instance.objects.exclude(pk=instance.pk).values_list('color', flat=True)

    # Получаем список доступных цветов, которые еще не использованы
    available_colors = [
        color.color_hex for color in colors_palette if color.color_hex not in used_colors
    ]

    if not available_colors:
        raise ValidationError({
            'color_error': _('Нет доступных цветов для группы')
        })

    return choice(available_colors)
