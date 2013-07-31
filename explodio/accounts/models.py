from django.contrib.auth import models as auth
from django.db import models

from explodio.accounts import managers


class User(auth.AbstractBaseUser, auth.PermissionsMixin):

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    username = models.CharField(max_length=50, unique=True, db_index=True)
    email = models.EmailField(null=True, blank=True)

    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = managers.UserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __unicode__(self):
        return self.get_full_name() or self.get_username()

    def get_full_name(self):
        return ' '.join(filter(bool, (self.first_name, self.last_name)))

    def get_short_name(self):
        return self.first_name
