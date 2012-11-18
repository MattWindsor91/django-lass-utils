"""Mixin adding range functions for models that have a defined time
range.

"""

import calendar


class DateRangeMixin(object):
    """Mixin adding range functions for models that have a defined
    datetime range.

    """

    ## MANDATORY OVERRIDES ##

    def range_start(self):
        """Returns the start of this item's datetime range.

        Must be overridden in descended classes.

        """
        raise NotImplementedError('start not implemented')

    def range_end(self):
        """Returns the end of this item's datetime range.

        Must be overridden in descended classes.

        """
        raise NotImplementedError('end not implemented')

    @classmethod
    def range_start_filter_arg(cls, inequality, value):
        """Given a filter inequality and a value to compare against,
        returns a tuple of the keyword argument and value that can
        be used to represent that inequality against the range start
        time in a filter.

        """
        raise NotImplementedError('start_filter_arg not implemented')

    @classmethod
    def range_end_filter_arg(cls, inequality, value):
        """Given a filter inequality and a value to compare against,
        returns a tuple of the keyword argument and value that can
        be used to represent that inequality against the range end
        time in a filter.

        """
        raise NotImplementedError('end_filter_arg not implemented')

    ## ADDITIONAL METHODS ##

    def date_range(self):
        """Returns both endpoints of this item's datetime range."""
        return self.range_start(), self.range_end()

    def range_duration(self):
        """Returns the duration of this item's datetime range."""
        return self.range_end() - self.range_start()

    def range_start_unix(self):
        """
        Returns the start of the range as a UNIX timestamp from UTC.

        """
        return calendar.timegm(self.range_start().utctimetuple())

    def range_end_unix(self):
        """
        Returns the end of the range as a UNIX timestamp from UTC.

        """
        return calendar.timegm(self.range_end().utctimetuple())
