from django.db import models
from django.utils.translation import gettext_lazy as _

from .validators import ShortURLValidator


class ShortLink(models.Model):
    """Модель для основных коротких ссылок"""
    original_link = models.URLField(
        unique=True,
        max_length=2000,
        verbose_name=_('Оригинальная ссылка'),
    )
    short_url = models.CharField(
        max_length=6,
        unique=True,
        db_index=True,
        verbose_name=_('Короткий код ссылки'),
        validators=[ShortURLValidator()]
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата создания')
    )

    class Meta:
        verbose_name = _('Короткая ссылка')
        verbose_name_plural = _('Короткие ссылки')

    def __str__(self):
        return self.original_link
