from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

from core.enums import Limits


class ShortURLValidator(RegexValidator):
    """Валидатор короткого кода ссылки"""
    regex = '^[a-zA-Z0-9]{}$'.format(Limits.MAX_LEN_LINK_SHORT_CODE.value)
    message = _('Короткий код ссылки недействителен')
    code = 'short_url_error'
