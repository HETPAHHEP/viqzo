from django.utils.translation import gettext_lazy as _
from rest_framework.validators import ValidationError

from core.enums import Limits


def check_links_group_constraints(group):
    """Проверка ограничений ссылок в группе"""
    if group:
        alias_links_count = group.short_group_links.filter(group=group).count()
        short_links_count = group.alias_group_links.filter(group=group).count()

        all_links_count = alias_links_count + short_links_count

        if all_links_count >= Limits.MAX_LINKS_GROUP_AMOUNT:
            raise ValidationError({
                'links_error': _(
                    'Превышено максимальное количество ссылок для этой группы.'
                )
            })
