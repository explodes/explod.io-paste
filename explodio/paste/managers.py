from django.utils import timezone

from explodio.common import managers


class PasteManager(managers.QuerySetManager):

    class QuerySet(managers.QuerySet):

        def by_ip_address(self, ip_address):
            return self.filter(ip_address=ip_address)

        def not_expired(self):
            now = timezone.now()
            return self.filter(expires_at__gt=now)

        def expired(self):
            now = timezone.now()
            return self.filter(expires_at__lte=now)
