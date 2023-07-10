from django.utils.translation import gettext_lazy as _
from rest_framework.validators import ValidationError


def check_campaign_group_constraints(instance):
    """Проверка ограничений группы в компании"""
    if instance.pk:
        # Редактирование существующей компании
        existing_group = instance.groups.objects.filter(
            name=instance.groups.name,
            owner=instance.owner,
        ).exclude(pk=instance.groups.pk).exists()
    else:
        # При создании новой компании
        existing_group = instance.groups.objects.filter(
            name=instance.groups.name,
            owner=instance.owner,
        ).exists()

    if existing_group:
        raise ValidationError(
            _('Такая группа уже существует в рамках компании.')
        )
