from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework.validators import ValidationError


def full_clean_check_validation_name(group):
    """Проверка ограничений ссылок у групп"""
    try:
        group.full_clean()  # Выполняем проверку перед сохранением
    except DjangoValidationError as e:

        if '__all__' in e.error_dict:
            raise ValidationError({
                'link_error': _('Ссылка уже находится в другой группе'),
                'original_error': e.error_dict,
            })
            # Если другие ошибки, просто передаем исключение дальше
        raise
