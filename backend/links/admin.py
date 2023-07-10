from django.contrib import admin

from .models import AliasShortLink, ShortLink


@admin.register(ShortLink)
class ShortURL(admin.ModelAdmin):
    list_display = ['original_link', 'short_url', 'clicks_count', 'created_at']
    search_fields = ['original_link', 'short_url']
    date_hierarchy = 'created_at'


@admin.register(AliasShortLink)
class AliasShortURL(admin.ModelAdmin):
    list_display = ['original_link', 'alias', 'clicks_count', 'created_at']
    search_fields = ['original_link', 'short_url']
    date_hierarchy = 'created_at'
