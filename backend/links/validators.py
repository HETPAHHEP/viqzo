from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

from core.enums import Limits


class ShortURLValidator(RegexValidator):
    """Валидатор короткого кода ссылки"""
    max_val = Limits.MAX_LEN_LINK_SHORT_CODE

    regex = fr'^[a-zA-Z0-9]{max_val}$'
    message = _('Короткий код ссылки недействителен.')
    code = 'short_url_error'


class AliasShortURLValidator(RegexValidator):
    """Валидатор пользовательского короткого кода ссылки"""
    min_val = Limits.MIN_LEN_ALIAS_CODE
    max_val = Limits.MAX_LEN_ALIAS_CODE

    regex = fr'^[a-zA-Z0-9]{min_val, max_val}$'
    message = _('Пользовательский код ссылки недействителен.')
    code = 'alias_url_error'


class HexColorValidator(RegexValidator):
    """Валидатор hex-кода цвета"""
    regex = r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'
    message = _('Цвет не соответствует hex кодировке.')
    code = 'invalid_hex_color'
