"""Models for bitemporal objects."""

from django.db import models
from django.db.models import query


class BitemporalQuerySet(query.QuerySet):
    """QuerySet for bitemporal model managers."""

    def valid(self):
        """Return objects that are currently valid."""
        return self.filter(valid_datetime_end__isnull=True)

    def valid_on(self, date_time):
        """Return objects that were valid on the given datetime."""
        condition = (
            models.Q(
                valid_datetime_start__lte=date_time,
                valid_datetime_end__gte=date_time) |
            models.Q(
                valid_datetime_start__lte=date_time,
                valid_datetime_end__isnull=True)
        )
        return self.filter(condition)


class BitemporalManager(models.Manager):
    """Model manager for bitemporal models."""

    def get_query_set(self):
        """Return an instance of `BitemporalQuerySet`."""
        return BitemporalQuerySet(self.model, using=self._db)

    #
    # Proxies to queryset
    #

    def valid(self):
        """Return queryset filtered to current valid objects."""
        return self.get_query_set().valid()

    def valid_on(self, date_time):
        """Return queryset filtered to objects valid on given datetime."""
        return self.get_query_set().valid_on(date_time)


class BitemporalModel(models.Model):
    """Base model class for bitemporal models."""

    valid_datetime_start = models.DateTimeField()
    valid_datetime_end = models.DateTimeField(blank=True, null=True)
    transaction_datetime_start = models.DateTimeField(auto_now_add=True)
    transaction_datetime_end = models.DateTimeField(blank=True, null=True)

    objects = BitemporalManager()

    class Meta:
        """Model options for `BitemporalModel`."""

        abstract = True
