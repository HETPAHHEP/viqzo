from core.enums import Limits
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .validators import ShortURLValidator


class ShortLink(models.Model):
    """Модель для основных коротких ссылок"""
    original_link = models.URLField(
        unique=True,
        max_length=Limits.MAX_LEN_ORIGINAL_LINK,
        verbose_name=_('Оригинальная ссылка'),
    )
    short_url = models.CharField(
        max_length=Limits.MAX_LEN_LINK_SHORT_CODE,
        unique=True,
        blank=True,
        db_index=True,
        verbose_name=_('Короткий код ссылки'),
        validators=[
            ShortURLValidator,
            MinValueValidator(
                limit_value=Limits.MAX_LEN_LINK_SHORT_CODE
            )
        ]
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата создания')
    )

    class Meta:
        verbose_name = _('Короткая ссылка')
        verbose_name_plural = _('Короткие ссылки')
        constraints = [
            models.UniqueConstraint(
                name='unique_link_shortcode',
                fields=['original_link', 'short_url'],
            )
        ]

    def __str__(self):
        return self.original_link
