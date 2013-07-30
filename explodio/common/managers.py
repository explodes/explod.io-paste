from datetime import datetime

from django.db import models
from django.db.models import query


QuerySet = query.QuerySet

class QuerySetManager(models.Manager):
    """
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

    """
    class QuerySet(QuerySet):
        """
        Place custom QuerySet filters here
        """
        pass

    def get_query_set(self):
        """
        Magic to use the inner-QuerySet
        :return: cls.QuerySet instance
        """
        qs = self.QuerySet(self.model, using=self._db)
        return qs

    def __getattr__(self, name, *args):
        """
        Magic to access the inner-QuerySet's filters
        :param name: attribute name
        :param args: __getattr__ *args
        :return: Value of attribute named name
        """
        if name.startswith('_'):
            raise AttributeError
        return getattr(self.get_query_set(), name, *args)


class ActiveQuerySet(QuerySet):
    """
    Special QuerySet that adds .active() and .inactive() filters
    """

    # Variable indicating active stateliness
    active_variable_name = 'active'

    def active(self):
        """
        Filter active instances
        :return: QuerySet of this QuerySet's model
        """
        return self.filter(**{self.active_variable_name:True})

    def inactive(self):
        """
        Filter inactive instances
        :return: QuerySet of this QuerySet's model
        """
        return self.filter(**{self.active_variable_name:False})


class ActiveQuerySetManager(QuerySetManager):
    """
    QuerySetManager with default ActiveQuerySet functionality
    """

    class QuerySet(ActiveQuerySet):
        """
        Built-in ActiveQuerySet magic
        """
        pass
