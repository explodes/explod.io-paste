from explodio.common import managers


class PasteManager(managers.QuerySetManager):

    class QuerySet(managers.QuerySet):

        def by_ip_address(self, ip_address):
            return self.filter(ip_address=ip_address)
