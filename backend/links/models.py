from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.enums import Limits

from . import validators
from .services.user_campaigns import check_campaign_group_constraints
from .services.user_groups import (check_group_constraints,
                                   check_links_group_constraints,
                                   set_color_for_group)
from .validators import HexColorValidator

User = get_user_model()


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
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('Владелец короткой ссылки'),
        related_name='short_owner',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _('Короткая ссылка')
        verbose_name_plural = _('Короткие ссылки')
        db_table = 'links_short_link'
        constraints = [
            models.UniqueConstraint(
                name='unique_link_shortcode',
                fields=['original_link', 'short_url'],
            )
        ]
        ordering = [
            'original_link', 'short_url', 'created_at',
            'clicks_count', 'last_clicked_at', 'is_active',
            'owner'
        ]

    def __str__(self):
        return self.short_url


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
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('Владелец пользовательской ссылки'),
        related_name='alias_owner',
        blank=True,
        null=True,
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
            'clicks_count', 'last_clicked_at', 'is_active',
            'owner'
        ]

    def __str__(self):
        return self.alias


class UserGroup(models.Model):
    """Пользовательская группа со ссылками пользователя"""
    name = models.CharField(
        max_length=Limits.MAX_LEN_GROUP_NAME.value,
        verbose_name=_('Имя группы'),
        unique=True,
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('Владелец группы'),
        related_name='group_owner',
    )
    color = models.CharField(
        max_length=7,
        validators=[HexColorValidator],
        default='',
        verbose_name=_('Цвет'),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата создания')
    )

    class Meta:
        verbose_name = _('Группа ссылок')
        verbose_name_plural = _('Группы ссылок')
        db_table = 'links_user_group'
        constraints = [
            models.UniqueConstraint(
                name='unique_name_per_owner',
                fields=['name', 'owner'],
                violation_error_message=_('Такая группа уже существует.')
            )
        ]

    def __str__(self):
        return self.name

    def clean(self):
        """Проверка ограничений"""
        check_group_constraints(UserGroup, self.owner)

    def set_color(self):
        return set_color_for_group(UserGroup, self)

    def save(self, *args, **kwargs):
        if not self.color:
            self.color = self.set_color()

        self.full_clean()  # Выполняем проверку перед сохранением
        super().save(*args, **kwargs)


class UserGroupLink(models.Model):
    """Ссылки в группе пользователя"""
    group = models.ForeignKey(
        UserGroup,
        on_delete=models.CASCADE,
        verbose_name=_('Группа пользователя'),
        related_name='group_link'
    )
    alias_link = models.ForeignKey(
        AliasShortLink,
        on_delete=models.CASCADE,
        verbose_name=_('Пользовательская ссылка группы'),
    )
    short_link = models.ForeignKey(
        ShortLink,
        on_delete=models.CASCADE,
        verbose_name=_('Короткая ссылка группы'),
    )

    class Meta:
        verbose_name = _('Группа ссылок')
        verbose_name_plural = _('Группы ссылок')
        db_table = 'links_user_group_with_links'
        constraints = [
            models.UniqueConstraint(
                name='unique_alias_link_per_group',
                fields=['group', 'alias_link'],
                violation_error_message=_('Пользовательская ссылка уже в другой группе')
            ),
            models.UniqueConstraint(
                name='unique_short_link_per_group',
                fields=['group', 'short_link'],
                violation_error_message=_('Короткая ссылка уже в другой группе')
            )
        ]

    def __str__(self):
        return self.name

    def clean(self):
        """Проверка ограничений"""
        check_links_group_constraints(UserGroupLink)

    def save(self, *args, **kwargs):
        self.full_clean()  # Выполняем проверку перед сохранением
        super().save(*args, **kwargs)


# КАМПАНИИ ДЛЯ ГРУПП. ПОКА НЕ РЕАЛИЗОВАНЫ ИЗ-ЗА СОМНЕНИЯ В НЕОБХОДИМОСТИ

# class UserCampaign(models.Model):
#     name = models.CharField(
#         max_length=Limits.MAX_LEN_CAMPAIGN_NAME.value,
#         verbose_name=_('Имя группы')
#     )
#     owner = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         verbose_name=_('Владелец компании'),
#         related_name='campaign_owner'
#     )
#     groups = models.ForeignKey(
#         UserGroup,
#         on_delete=models.CASCADE,
#         verbose_name=_('Группы компании'),
#         related_name="groups",
#         related_query_name="group",
#     )
#
#     class Meta:
#         verbose_name = _('Компания')
#         verbose_name_plural = _('Компании')
#         db_table = 'links_user_campaign'
#         constraints = [
#             models.UniqueConstraint(
#                 name='unique_campaign_name_per_owner',
#                 fields=['name', 'owner'],
#                 violation_error_message=_(
#                     'Такая компания уже существует.'
#                 )
#             )
#         ]
#
#     def __str__(self):
#         return self.name
#
#     def clean(self):
#         """Проверка ограничений"""
#         check_campaign_group_constraints(self)
#
#     def save(self, *args, **kwargs):
#         self.full_clean()  # Выполняем проверку перед сохранением
#         super().save(*args, **kwargs)
