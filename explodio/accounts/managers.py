from django.contrib.auth import models as auth
from django.utils import timezone

from explodio.common import managers


class UserManager(auth.BaseUserManager, managers.ActiveQuerySetManager):

    class QuerySet(managers.ActiveQuerySet):

        active_variable_name = 'is_active'

    def create_user(self, username, password=None, commit=True, **extra_fields):
        if not username:
            raise ValueError('Username must be set')
        user = self.model(
            username=username,
            is_staff=False,
            is_superuser=False,
            **extra_fields
        )
        user.date_joined = timezone.now()
        user.is_active = True
        user.set_password(password)
        if commit:
            user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        user = self.create_user(username, password, commit=False, **extra_fields)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save()
        return user
