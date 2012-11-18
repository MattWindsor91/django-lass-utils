"""A partial implementation of DateRangeMixin's interface by which
the date range is fulfilled by an 'effective from' and an 'effective
to' pair of fields.

"""

from django.db import models
from django.utils import timezone
from lass_utils.mixins.date_range import DateRangeMixin


class EffectiveRangeMixin(models.Model, DateRangeMixin):
    """Mixin adding an 'effective from' and 'effective to' pair of
    fields that implement DateRangeMixin.

    """

    class Meta:
        get_latest_by = 'effective_from'
        abstract = True

    effective_from = models.DateTimeField(
        db_column='effective_from',
        null=True,
        blank=True,
        default=timezone.now(),
        help_text="""The date from which this item applies.
            If this is not given, then the item is inert, which
            is usually the case when it has not been approved.

            """)

    effective_to = models.DateTimeField(
        db_column='effective_to',
        null=True,
        blank=True,
        help_text="""The date on which this credit ceases to apply,
            if any.

            """)

    def range_start(self):
        return self.effective_from

    def range_end(self):
        return self.effective_to

    @classmethod
    def in_range(cls, from_date, to_date, queryset=None):
        """Retrieves (or filters towards) a QuerySet of items in
        this model that are effective during the given time
        range.

        The items must cover the entire range.

        Items with an 'effective_from' of NULL will be discarded;
        items with an 'effective_to' of NULL will be treated as if
        their effective_to is infinitely far in the future.

        If queryset is given, it will be filtered with the
        above condition; else the entire object set will be
        considered.
        """
        if queryset is None:
            queryset = cls.objects.all()
        # Note that filter throws out objects with fields set to
        # NULL whereas exclude does not.
        return (queryset
                .filter(effective_from__lte=from_date)
                .exclude(effective_to__lt=to_date))

    @classmethod
    def at(cls, date, *args, **kwargs):
        """Wrapper around 'in_range' that retrieves items effective
        at the given moment in time.

        See the documentation for 'in_range' for information about
        which arguments can be provided besides 'date'.

        """
        return cls.in_range(date, date, *args, **kwargs)
