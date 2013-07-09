from django.contrib import admin

from explodio.paste import models as paste


class PasteAdmin(admin.ModelAdmin):
    list_display = ('title', 'language', 'style')
    list_filter = ('language', 'style')
    date_hierarchy = 'created_at'
    search_fields = ('title', 'ip_address')

    readonly_fields = ('modified_at', 'created_at', 'expires_at')

admin.site.register(paste.Paste, PasteAdmin)
