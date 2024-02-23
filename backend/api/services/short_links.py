from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework.validators import ValidationError

from links.models import AliasShortLink, ShortLink

from .url_short_logic import LinkHash

User = get_user_model()


def create_link(
        valid_data: dict,
        user: User | None = None) -> tuple[ShortLink, bool]:
    """Создание сокращенной ссылки для оригинальной"""
    original_link = valid_data.get('original_link')
    alias = valid_data.get('alias')
    group = valid_data.get('group')

    if alias:
        link = ShortLink(
            original_link=original_link,
            short=alias,
        )

        link.save()
        created = True

    else:
        link, created = ShortLink.get_or_create(
            original_link=original_link
        )

    if created and not alias:
        while not link.short:
            # проверяем, не занят ли короткий код и присваиваем его ссылке
            short_code = LinkHash().get_short_code()

            if not ShortLink.objects.filter(short=short_code).exists():
                link.short_url = short_code
                link.save()

    if created and user:
        if group:
            link.group = group

        link.owner = user
        link.save()

    return link, created


def validate_alias(data):
    alias = data.get('alias')

    if alias:

        if ShortLink.objects.filter(short=alias).exists():
            raise ValidationError({
                'alias_error': _('Данный код для ссылки уже занят.')
            })

    return data


def validate_group_for_link(data, user):
    """Проверка условий для изменения ссылки"""
    group = data.get('group')

    if group:
        if group.owner != user:
            raise ValidationError({
                'group_error': _(
                    "Нельзя добавить ссылку в группу, так как Вы не являетесь её владельцем."
                )
            })

    return data
