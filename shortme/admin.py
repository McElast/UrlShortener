from django.contrib import admin
from .models import ShortenUrl


@admin.register(ShortenUrl)
class ShortenUrlAdmin(admin.ModelAdmin):
    """
    Отображение модели ShortenUrl в админ панели
    """
    list_display = ('original_url', 'short_url_part', 'client_session', 'added')
    fields = ('original_url', 'short_url_part', 'client_session')
    list_filter = ('original_url', )
    search_fields = ('original_url', )
    list_display_links = ('original_url', 'short_url_part')
