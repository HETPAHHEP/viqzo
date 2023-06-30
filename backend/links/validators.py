from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class ShortURLValidator(RegexValidator):
    """Валидатор короткого кода ссылки"""
    regex = r'^[a-zA-Z0-9]+$'
    message = _('Короткий код ссылки недействителен')
    code = 'short_url_error'
