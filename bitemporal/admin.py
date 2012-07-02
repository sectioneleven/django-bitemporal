"""`ModelAdmin` classes for `BitemporalModel` models."""

from django.contrib import admin


class BitemporalModelAdmin(admin.ModelAdmin):
    """`ModelAdmin` class for `BitemporalModel` models."""

    def get_list_display(self, *args, **kwargs):
        """Append `BitemporalModel` fields to `ModelAdmin` `list_display`."""
        list_display = super(
            BitemporalModelAdmin, self).get_list_display(*args, **kwargs)
        return list(list_display) + [
            'valid_datetime_start', 'valid_datetime_end',
            'transaction_datetime_start', 'transaction_datetime_end']
