from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from explodio.accounts import models


class CustomUserAdmin(UserAdmin):
    pass

admin.site.register(models.User, UserAdmin)
