from django.utils.translation import gettext_lazy as _
from rest_framework.validators import ValidationError


def validate_links_for_group(data, user):
    short_link = data.get('short_link')
    alias_link = data.get('alias_link')

    if not short_link and not alias_link:
        raise ValidationError({
            'links_error': _(
                "Необходимо передать одно из полей 'short_link' или 'alias_link'."
            )
        })

    if short_link and alias_link:
        raise ValidationError({
            'links_error': _(
                "Необходимо передать только одно из полей 'short_link' или 'alias_link'."
            )
        })

    if short_link:
        if short_link.owner != user:
            raise ValidationError({
                'links_error': _(
                    "Нельзя добавить 'short_link' ссылку в группу, так как Вы не являетесь её владельцем."
                )
            })

    if alias_link:
        if alias_link.owner != user:
            raise ValidationError({
                'links_error': _(
                    "Нельзя добавить 'alias_link' ссылку в группу, так как Вы не являетесь её владельцем"
                )
            })

    return data
