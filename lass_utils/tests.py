"""
Test suite for the ``lass_utils`` package.

"""

from django.test import TestCase

from lass_utils.models import Type


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
