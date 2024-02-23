from django.utils.translation import gettext_lazy as _
from rest_framework.validators import ValidationError

from core.enums import Limits


def check_links_group_constraints(group):
    """Проверка ограничений ссылок в группе"""
    if group:
        links_count = group.group_links.count()

        if links_count >= Limits.MAX_LINKS_GROUP_AMOUNT:
            raise ValidationError({
                'links_error': _(
                    'Превышено максимальное количество ссылок для этой группы.'
                )
            })
