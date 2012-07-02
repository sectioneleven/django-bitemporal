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

    def __getattr__(self, attr, *args):
        """Return attributes from queryset."""
        try:
            return getattr(self.__class__, attr, *args)
        except (AttributeError,) as e:
            try:
                # return attribute from queryset
                return getattr(self.get_query_set(), attr, *args)
            except AttributeError:
                # attribute not found in queryset instance;
                # raise original `AttributeError` exception
                raise e


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
