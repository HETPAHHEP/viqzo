from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.enums import Limits

from . import validators


class BaseShortLink(models.Model):
    """Базовая модель для коротких ссылок"""
    original_link = models.URLField(
        unique=True,
        max_length=Limits.MAX_LEN_ORIGINAL_LINK.value,
        verbose_name=_('Оригинальная ссылка'),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата создания')
    )
    clicks_count = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Переходов по ссылке')
    )
    last_clicked_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Последнее время клика')
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Активна ли ссылка?')
    )

    def save(self, *args, **kwargs):
        if self.pk:
            if self.clicks_count == 0:
                # Кликов ещё не было
                self.last_clicked_at = None
            else:
                # Обновляем время последнего клика при переходе
                self.last_clicked_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.original_link

    class Meta:
        abstract = True


class ShortLink(BaseShortLink):
    """Модель для основных коротких ссылок"""
    short_url = models.CharField(
        max_length=Limits.MAX_LEN_LINK_SHORT_CODE.value,
        unique=True,
        blank=True,
        db_index=True,
        verbose_name=_('Короткий код ссылки'),
        validators=[
            validators.ShortURLValidator,
            MinValueValidator(
                limit_value=Limits.MAX_LEN_LINK_SHORT_CODE.value
            )
        ]
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
        ordering = [
            'original_link', 'short_url', 'created_at',
            'clicks_count', 'last_clicked_at', 'is_active'
        ]


class AliasShortLink(BaseShortLink):
    """Модель для основных коротких ссылок"""
    original_link = models.URLField(
        max_length=Limits.MAX_LEN_ORIGINAL_LINK.value,
        verbose_name=_('Оригинальная ссылка'),
    )
    alias = models.CharField(
        max_length=Limits.MAX_LEN_ALIAS_CODE.value,
        unique=True,
        blank=True,
        db_index=True,
        verbose_name=_('Пользовательское имя ссылки'),
        validators=[
            validators.AliasShortURLValidator,
            MinValueValidator(
                limit_value=Limits.MIN_LEN_ALIAS_CODE.value
            )
        ]
    )

    class Meta:
        verbose_name = _('Пользовательская ссылка')
        verbose_name_plural = _('Пользовательские ссылки')
        db_table = 'links_alias_link'
        constraints = [
            models.UniqueConstraint(
                name='unique_alias_link',
                fields=['original_link', 'alias'],
            )
        ]
        ordering = [
            'original_link', 'alias', 'created_at',
            'clicks_count', 'last_clicked_at', 'is_active'
        ]
