from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

from core.enums import Limits


class AliasCodeValidator(RegexValidator):
    """Валидатор пользовательского короткого кода ссылки"""

    min_val = Limits.MIN_LEN_LINK_SHORT_CODE
    max_val = Limits.MAX_LEN_LINK_SHORT_CODE

    regex = rf"^[a-zA-Z0-9]{{{min_val},{max_val}}}$"
    message = _("Пользовательский код ссылки недействителен.")
    code = "alias_url_error"
