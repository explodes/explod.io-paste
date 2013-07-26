import random

from django.db import models
from django.utils import timezone

from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.styles import get_all_styles

from explodio.paste import managers


LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted(((item[1][0], item[0]) for item in LEXERS), key=lambda x: x[1].lower())
STYLE_CHOICES = sorted(((item, item) for item in get_all_styles()), key=lambda x: x[1].lower())

class Paste(models.Model):

    title = models.CharField(max_length=64)
    slug = models.CharField(max_length=128, unique=True, db_index=True)
    language = models.CharField(choices=LANGUAGE_CHOICES,
                                default='python',
                                max_length=100)
    style = models.CharField(choices=STYLE_CHOICES,
                             default='monokai',
                             max_length=100)
    code = models.TextField()
    highlighted = models.TextField()

    ip_address = models.IPAddressField()
    expires_at = models.DateTimeField()
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = managers.PasteManager()

    class Meta:
        ordering = ('created_at',)

    def save(self, *args, **kwargs):
        """
        Use the `pygments` library to create a highlighted HTML
        representation of the code snippet.
        """
        if not self.slug:
            self.slug = '%02x' % random.getrandbits(256)

        lexer = get_lexer_by_name(self.language)
        options = self.title and {'title': self.title} or {}
        formatter = HtmlFormatter(style=self.style, linenos='table',
                                  full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)
        super(Paste, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

    @property
    def expired(self):
        now = timezone.now()
        return self.expires_at <= now

    @models.permalink
    def get_absolute_url(self):
        return 'paste:paste', (), {'slug' : self.slug}
