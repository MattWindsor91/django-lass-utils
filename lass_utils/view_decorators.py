"""View decorators.

These can simplify view code.
Other functions too?
"""

import datetime


def date_normalise(view):
    """A view decorator that interprets incoming date data.

    Decorates a view
    Converts many date formats
    Sends the view one date

    If no arguments whatsoever besides the request are given, the current day
    is used.

    Args:
        view: the view function to decorate, which should take as its sole
            parameters a request and a date.

    Returns:
        the decorated view, which accepts both dates (as the start parameter)
        as well as combinations of the integral/string arguments year, week,
        weekday, month and day.

    """
    def new_view(request,
                 start=None,
                 year=None,
                 week=None,
                 weekday=None,
                 month=None,
                 day=None):
        if start:
            # Strip any time information
            if hasattr(start, 'date'):
                start = start.date()
        else:
            if year and month:
                start = datetime.date(
                    int(year),
                    int(month),
                    int(day) if day else 1  # Default to the 1st
                )
            elif year and week:
                start = iso_to_gregorian(
                    int(year),
                    int(week),
                    int(weekday) if weekday else 1  # Default to Monday
                )
            elif not any([start, year, week, weekday, month, day]):
                start = datetime.date.today()
            else:
                raise ValueError(
                    "Incorrect combination of arguments to view."
                )
        return view(request, start)
    return new_view


## Helper functions

## These next two functions were purloined from
## http://stackoverflow.com/q/304256

def iso_year_start(iso_year):
    """The gregorian calendar date of the first day of the given ISO year.
    """
    fourth_jan = datetime.date(iso_year, 1, 4)
    delta = datetime.timedelta(fourth_jan.isoweekday()-1)
    return fourth_jan - delta


def iso_to_gregorian(iso_year, iso_week, iso_day):
    """Gregorian calendar date for the given ISO year, week and day.
    """
    year_start = iso_year_start(iso_year)
    return year_start + datetime.timedelta(
        days=iso_day-1,
        weeks=iso_week-1
    )
