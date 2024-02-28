from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework.validators import ValidationError

from core.enums import Limits

from .url_short_logic import LinkHash


def get_short_code(model_link):
    """Установка обычного короткого кода ссылки, если нет alias"""
    while True:
        short_code = LinkHash().get_short_code()

        if not model_link.objects.filter(short=short_code).exists():
            return short_code


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


def full_clean_check_validation_short(group):
    """Проверка ограничений имени у групп"""
    try:
        group.full_clean()  # Выполняем проверку перед сохранением
    except DjangoValidationError as e:
        if 'short' in e.error_dict:
            raise ValidationError({
                'short_error': e.error_dict['short']
            })

        if '__all__' in e.error_dict:
            raise ValidationError({
                'original_error': e.error_dict,
            })
            # Если другие ошибки, просто передаем исключение дальше
        raise
