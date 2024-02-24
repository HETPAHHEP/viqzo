from django.contrib import admin

from .models import ShortLink


@admin.register(ShortLink)
class ShortURL(admin.ModelAdmin):
    list_display = ['original_link', 'short', 'clicks_count', 'created_at']
    search_fields = ['original_link', 'short']
    date_hierarchy = 'created_at'
