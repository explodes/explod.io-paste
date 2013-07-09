from django.core.management import base

from explodio.paste import models as paste


class Command(base.NoArgsCommand):

    help = "Delete expired pastes."

    def handle(self, *args, **kwargs):
        paste.Paste.objects.expired().delete()
