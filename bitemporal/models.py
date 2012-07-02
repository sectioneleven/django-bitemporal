"""Models for bitemporal objects."""

from django.db import models


class BitemporalModel(models.Model):
    """Base model class for bitemporal models."""

    valid_datetime_start = models.DateTimeField()
    valid_datetime_end = models.DateTimeField(blank=True, null=True)
    transaction_datetime_start = models.DateTimeField(auto_now_add=True)
    transaction_datetime_end = models.DateTimeField(blank=True, null=True)

    class Meta:
        """Model options for `BitemporalModel`."""

        abstract = True
