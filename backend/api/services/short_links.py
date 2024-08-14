from django.utils.translation import gettext_lazy as _
from rest_framework.validators import ValidationError

from links.models import ShortLink


def validate_alias(data):
    alias = data.get("alias")

    if alias and ShortLink.objects.filter(short=alias).exists():
        raise ValidationError(
            {"alias_error": _("Данный код для ссылки уже занят.")}
        )

    return data


def validate_group_for_link(data, user):
    """Проверка условий для изменения ссылки"""
    group = data.get("group")

    if group and group.owner != user:
        raise ValidationError(
            {
                "group_error": _(
                    "Нельзя добавить ссылку в группу, "
                    "так как Вы не являетесь её владельцем."
                )
            }
        )

    return data
