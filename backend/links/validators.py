from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

from core.enums import Limits


class ShortCodeValidator(RegexValidator):
    """Валидатор короткого кода ссылки"""

    max_val = Limits.BASIC_LEN_SHORT_CODE

    regex = rf"^[a-zA-Z0-9]{max_val}$"
    message = _("Короткий код ссылки недействителен.")
    code = "short_url_error"


class HexColorValidator(RegexValidator):
    """Валидатор hex-кода цвета"""

    regex = r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"
    message = _("Цвет не соответствует hex кодировке.")
    code = "invalid_hex_color"
