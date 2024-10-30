import re
from re import Pattern
from dataclasses import dataclass

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


@dataclass
class Link:
    link: str
    alias: str

    LINK_REGEX: Pattern = re.compile(
        r"(^$|(http(s)?://)([\w-]+\.)+[\w-]+([\w- ;,./?%&=]*))"
    )

    def __post_init__(self):
        if not self.is_valid_link(self.link):
            raise ValueError("Недопустимый формат ссылки")

        if self.alias:
            AliasCodeValidator()(self.alias)

    @classmethod
    def is_valid_link(cls, link) -> bool:
        return bool(cls.LINK_REGEX.match(link))
