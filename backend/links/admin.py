from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import Color, ShortLink, UserGroup


@admin.register(ShortLink)
class ShortLinkAdmin(admin.ModelAdmin):
    list_display = [
        "original_link",
        "owner",
        "short",
        "clicks_count",
        "created_at",
    ]
    search_fields = ["original_link", "short"]
    date_hierarchy = "created_at"


@admin.register(UserGroup)
class UserGroupAdmin(admin.ModelAdmin):
    list_display = ["name", "owner", "colored_hex"]
    search_fields = ["owner", "name"]
    date_hierarchy = "created_at"

    def colored_hex(self, obj):
        """Демонстрация цвета в панели"""
        return format_html(
            f'<span style="color: {obj.color};">{obj.color}</span>'
        )

    colored_hex.short_description = _("Показ цвета")


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "colored_hex"]
    search_fields = ["name", "color_hex"]
    search_help_text = "Поиск цвета по названию и HEX"
    ordering = ["name"]

    def colored_hex(self, obj):
        """Демонстрация цвета в панели"""
        return format_html(
            f'<span style="color: {obj.color_hex};">{obj.color_hex}</span>'
        )

    colored_hex.short_description = _("Показ цвета")
