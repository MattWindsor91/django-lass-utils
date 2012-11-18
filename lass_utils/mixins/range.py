"""Mixin adding range functions for models that have a defined time
range.

"""


class RangeMixin(object):
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

    ## ADDITIONAL METHODS ##

    def date_range(self):
        """Returns both endpoints of this item's datetime range."""
        return self.range_start(), self.range_end()

    def range_duration(self):
        """Returns the duration of this item's datetime range."""
        return self.range_end() - self.range_start()
