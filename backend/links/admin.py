from django.contrib import admin

from .models import ShortLink


@admin.register(ShortLink)
class ShortURL(admin.ModelAdmin):
    list_display = ['original_link', 'short_url', 'created_at']
    search_fields = ['original_link', 'short_url']
    date_hierarchy = 'created_at'
