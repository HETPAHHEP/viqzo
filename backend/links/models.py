from django.contrib.auth import get_user_model
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.enums import Limits

from . import validators
from .services.short_links import (check_links_group_constraints,
                                   full_clean_check_validation_short,
                                   get_short_code)
from .services.user_groups import (check_group_constraints,
                                   full_clean_check_validation_name,
                                   set_color_for_group)

User = get_user_model()


class UserGroup(models.Model):
    """Пользовательская группа со ссылками пользователя"""
    name = models.CharField(
        max_length=Limits.MAX_LEN_GROUP_NAME,
        verbose_name=_('Имя группы'),
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('Владелец группы'),
        related_name='group_owner',
    )
    color = models.CharField(
        max_length=7,  # Hex format with '#'
        validators=[
            validators.HexColorValidator
        ],
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
        """Поставить цвет группе"""
        return set_color_for_group(UserGroup, self)

    def try_full_clean(self):
        """Запустить проверку полей модели"""
        return full_clean_check_validation_name(self)

    def save(self, *args, **kwargs):
        if not self.color:
            self.color = self.set_color()

        self.try_full_clean()

        super().save(*args, **kwargs)


class ShortLink(models.Model):
    """Модель для коротких ссылок"""
    original_link = models.URLField(
        max_length=Limits.MAX_LEN_ORIGINAL_LINK,
        verbose_name=_('Оригинальная ссылка'),
    )
    short = models.CharField(
        max_length=Limits.MAX_LEN_LINK_SHORT_CODE,
        unique=True,
        db_index=True,
        verbose_name=_('Короткий код ссылки'),
        validators=[
            validators.ShortCodeValidator,
            MinLengthValidator(
                limit_value=Limits.MIN_LEN_LINK_SHORT_CODE
            ),
            MaxLengthValidator(
                limit_value=Limits.MAX_LEN_LINK_SHORT_CODE
            )
        ]
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата создания'),
        editable=False,
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
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('Владелец короткой ссылки'),
        related_name='link_owner',
        blank=True,
        null=True,
    )
    group = models.ForeignKey(
        UserGroup,
        db_column='group',
        on_delete=models.SET_NULL,
        verbose_name=_('Группа пользователя'),
        related_name='group_links',
        blank=True,
        null=True,
    )

    def set_short(self):
        """Поставить короткий код для ссылки, если нет alias"""
        return get_short_code(self.__class__)

    def clean(self):
        """Проверка ограничений ссылки"""
        check_links_group_constraints(self.group)

    def try_full_clean(self):
        """Запустить проверку полей модели"""
        return full_clean_check_validation_short(self)

    def save(self, *args, **kwargs):
        """Сохранить ссылку"""
        if not self.short:
            self.short = self.set_short()

        if 'clean' in dir(self):
            self.try_full_clean()

        if self.pk:
            if self.clicks_count == 0:
                # Кликов ещё не было
                self.last_clicked_at = None
            else:
                # Обновляем время последнего клика при переходе
                self.last_clicked_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"link: {self.original_link} short: {self.short}"

    class Meta:
        verbose_name = _('Короткая ссылка')
        verbose_name_plural = _('Короткие ссылки')
        db_table = 'links_short_link'


# КАМПАНИИ ДЛЯ ГРУПП. ПОКА НЕ РЕАЛИЗОВАНЫ ИЗ-ЗА СОМНЕНИЯ В НЕОБХОДИМОСТИ

# class UserCampaign(models.Model):
#     name = models.CharField(
#         max_length=Limits.MAX_LEN_CAMPAIGN_NAME,
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
