from datetime import datetime

from django.db import models
from django.db.models import query


QuerySet = query.QuerySet

class QuerySetManager(models.Manager):
    '''
    Lets custom filters become chained on a manager.

    E.x.

    class FooManager(QuerySetManager):

        class QuerySet(django.db.models.query.QuerySet):

            def foo_filter(self):
                return self.filter(foo__gte=3)

            def bar_filter(self):
                return self.filter(bar__isnull=False)


    class Foo(Model):
       ...
       objects = FooManager()
       ...

    queryset = Foo.objects.foo_filter().bar_filter()

    '''
    class QuerySet(QuerySet):
        pass

    def get_query_set(self):
        qs = self.QuerySet(self.model, using=self._db)
        return qs

    def __getattr__(self, name, *args):
        if name.startswith('_'):
            raise AttributeError
        return getattr(self.get_query_set(), name, *args)


class ActiveQuerySet(QuerySet):

    def active(self):
        return self.filter(active=True)

    def inactive(self):
        return self.filter(active=False)


class ActiveQuerySetManager(QuerySetManager):

    class QuerySet(ActiveQuerySet):
        pass
