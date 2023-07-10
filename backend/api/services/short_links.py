from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework.validators import ValidationError

from links.models import AliasShortLink, ShortLink

from .url_short_logic import LinkHash

User = get_user_model()


def create_link(
        valid_data: dict,
        user: User | None = None) -> tuple[ShortLink | AliasShortLink, bool]:
    """Создание сокращенной ссылки для оригинальной"""
    original_link = valid_data.get('original_link')
    alias = valid_data.get('alias')

    if alias:
        url = AliasShortLink.objects.create(
            original_link=original_link,
            alias=alias,
        )
        created = True

    else:
        url, created = ShortLink.objects.get_or_create(
            original_link=original_link
        )

    if created and not alias:
        while not url.short_url:
            # проверяем, не занят ли короткий код и присваиваем его ссылке
            short_code = LinkHash().get_short_code()

            if not ShortLink.objects.filter(short_url=short_code).exists():
                url.short_url = short_code
                url.save()

    if user:
        url.owner = user
        url.save()

    return url, created


def validate_alias(data):
    alias = data.get('alias')

    if alias:

        if AliasShortLink.objects.filter(alias=alias).exists():
            raise ValidationError({
                'alias_error': _('Данный код для ссылки уже занят.')
            })

    return data
