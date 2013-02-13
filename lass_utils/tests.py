"""
Test suite for the ``lass_utils`` package.

"""

import datetime

from django.test import TestCase

from lass_utils.models import Type
from lass_utils import view_decorators


@view_decorators.date_normalise
def fake_view(request, date):
    """Mock view for the test case.

    This is not a view
    It returns its argument
    So it can be checked
    """

    return date


class DateNormaliseTest(TestCase):
    """Tests the date_normalise decorator.

    Test date_normalise
    Make sure it can interpret
    All those date formats
    """
    def setUp(self):
        """Sets up the test fixture."""
        self.today = datetime.date.today()
        self.date = datetime.date(day=13, month=2, year=1993)
        self.datetime = datetime.datetime(
            day=13, month=2, year=1993, hour=13, minute=50, second=0
        )

    def assert_dates_equal(self, f):
        """Checks f to see if it preserves dates.

        Make sure the function
        When passed a date or datetime
        Yields it as a date
        """
        self.assertEqual(self.date, f(self.date))
        self.assertEqual(self.datetime.date(), f(self.datetime))

    def assert_returns_month(self, f):
        """Asserts f, given a date, returns the First of that date's month.

        Make sure the result
        Of dates and datetimes passed is
        The first of their months
        """
        (
            self.assertEqual(f(d), d.replace(day=1))
            for d in (self.date, self.datetime)
        )

    def assert_returns_week(self, f):
        """Asserts f, given a date, returns Monday of the week of that date.

        Make sure the result
        Of dates and datetimes passed is
        Monday of their weeks
        """
        for date in self.date, self.datetime:
            fdate = f(date).isocalendar()
            self.assertEqual(fdate[:2], date.isocalendar()[:2])
            self.assertEqual(fdate[2], 1)

    def test_assert_soundness(self):
        """Ensures our assertion functions are sound.

        These asserts should work
        On these trivial functions
        If they work at all
        """
        def dates_equal_test(x):
            """Test function for assert_dates_equal.

            This function returns
            Dates unmodified; datetimes
            Reduced to their dates
            """
            return x.date() if hasattr(x, 'date') else x
        self.assert_dates_equal(dates_equal_test)

        def returns_month_test(x):
            """Test function for assert_returns_month.

            For dates and datetimes
            I strip down to date, and set
            The day to the First
            """
            if hasattr(x, 'date'):
                x = x.date()
            return x.replace(day=1)
        self.assert_returns_month(returns_month_test)

        def returns_week_test(x):
            """Test function for assert_returns_week.

            For dates and datetimes
            I strip down to date, and set
            The day to Monday
            """
            if hasattr(x, 'date'):
                x = x.date()
            # Skip to the Monday of this date's start week by removing
            # the number of days since Monday from the date
            _, _, day = x.isocalendar()
            x = x - datetime.timedelta(days=day - 1)
            return x
        self.assert_returns_week(returns_week_test)

    def test_start(self):
        """Ensures that fake_view(start=date) works correctly.
        """
        self.assert_dates_equal(lambda d: fake_view(None, start=d))

    def test_year_month_day(self):
        """Ensures that fake_view(year=y, month=m, day=d) works correctly.
        """
        self.assert_dates_equal(
            lambda d: fake_view(None, year=d.year, month=d.month, day=d.day)
        )

    def test_year_month(self):
        """Ensures that fake_view(year=y, month=m) works correctly.
        """
        self.assert_returns_month(
            lambda d: fake_view(None, year=d.year, month=d.month)
        )

    def test_year_week_weekday(self):
        """Ensures that fake_view(year=y, week=w, weekday=d) works correctly.
        """
        self.assert_dates_equal(
            lambda d: fake_view(
                None,
                **(dict(zip(('year', 'week', 'weekday'), d.isocalendar())))
            )
        )

    def test_year_week(self):
        """Ensures that fake_view(year=y, week=w) works correctly.
        """
        self.assert_returns_week(
            lambda d: fake_view(
                None,
                **(dict(zip(('year', 'week'), d.isocalendar()[:2])))
            )
        )


class ConcreteType(Type):
    """
    A concrete model that extends `Type`, used for testing.

    """
    pass


class TypeTest(TestCase):
    """
    Tests the `Type` abstract model.

    """
    fixtures = ['type_test']

    def setUp(self):
        """
        Sets up the test fixture.

        """
        pass

    def test_get(self):
        """
        Tests that using `get` on an existing type retrieves it as
        expected.

        """
        test_objs = list(ConcreteType.objects.all())
        assert len(test_objs) > 1, 'Test fixture should not be empty.'

        for obj in test_objs:
            # Passing an object to its own class's get should
            # just return the object unmolested
            self.assertIs(ConcreteType.get(obj), obj)
            # Getting an object by its name should work
            self.assertEqual(ConcreteType.get(obj.name), obj)
            # As should getting an object by its primary key
            self.assertEqual(ConcreteType.get(obj.pk), obj)

    def test_get_if_exists(self):
        """
        Tests that using `get_if_exists` on an existing type retrieves it as
        expected.

        """
        test_objs = list(ConcreteType.objects.all())
        assert len(test_objs) > 1, 'Test fixture should not be empty.'

        for obj in test_objs:
            # Passing an object to its own class's get should
            # just return the object unmolested
            self.assertIs(ConcreteType.get_if_exists(obj), obj)
            # Getting an object by its name should work
            self.assertEqual(ConcreteType.get_if_exists(obj.name), obj)
            # As should getting an object by its primary key
            self.assertEqual(ConcreteType.get_if_exists(obj.pk), obj)

        # These should return None
        self.assertIsNone(ConcreteType.get_if_exists(-1))
        self.assertIsNone(ConcreteType.get_if_exists('notDefined'))

        with self.assertRaises(TypeError):
            ConcreteType.get({'cannot': 'pass', 'a': 'dict'})

    def test_get_fail(self):
        """
        Tests that using `get` with erroneous arguments behaves
        correctly.

        """
        with self.assertRaises(ConcreteType.DoesNotExist):
            ConcreteType.get(-1)

        with self.assertRaises(ConcreteType.DoesNotExist):
            ConcreteType.get('thisWillHopefullyNotBeDefined')

        with self.assertRaises(TypeError):
            ConcreteType.get({'cannot': 'pass', 'a': 'dict'})
