from django.db import models
from django.utils.translation import gettext_lazy as _
from validators import ShortURLValidator


class ShortLink(models.Model):
    """Model for basic short links"""
    original_url = models.URLField(
        unique=True,
        verbose_name=_('Original link'),
    )
    short_code = models.CharField(
        max_length=6,
        unique=True,
        verbose_name=_('Short link code'),
        validators=[ShortURLValidator()]
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Date of creation')
    )
