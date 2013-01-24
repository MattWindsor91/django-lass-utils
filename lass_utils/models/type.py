"""
Type
----

This module defines :class:`type`, a common base class for type-of
models.

In `LASS`, the pattern of dynamic lookup tables representing types
and categories of other objects is very prevalent; in order to make
using these type models more convenient, we have a common abstract
base class for them.

"""

from django.db import models
from django.core.cache import cache
from django.http import Http404


class Type(models.Model):
    """
    An abstract base class for models representing types, categories
    or other keyed collections of other models.

    """
    name = models.SlugField(
        help_text="""The short name of this type entry, which should
            be used to identify it in code.

            """)
    description = models.TextField(
        help_text="""A human-readable description of this type entry
            and its semantics.

            """)

    ## MAGIC METHODS ##

    def __unicode__(self):
        """
        Returns a Unicode representation of this type.

        :rval: unicode

        """
        return self.name

    ## CLASS METHODS ##

    @classmethod
    def get_if_exists(cls, identifier):
        """
        Like :meth:`get`, but returns ``None`` instead of raising an
        exception if the requested type does not exist.

        TypeError is still raised in the event of a disallowed
        identifier type.

        :param identifier: an item of data representing the type to
            retrieve, or the type itself
        :type identifier: string, integer or an element of the called
            class
        :rtype: an element of the called class

        """
        try:
            result = cls.get(identifier)
        except cls.DoesNotExist:
            result = None
        return result


    @classmethod
    def get(cls, identifier):
        """
        User-friendly type get function.

        This function uses the caching system to cache the type for
        a short amount of time.

        If the input is an integer, it will be treated as the target
        type's primary key.

        If the input is a string, it will be treated as the target
        type's name (case-insensitively).

        If the input is an instance of cls itself, it will simply be
        returned.

        Else, TypeError will be raised.

        :param identifier: an item of data representing the type to
            retrieve, or the type itself
        :type identifier: string, integer or an element of the called
            class
        :rtype: an element of the called class
        """
        if isinstance(identifier, cls):
            result = identifier
        else:
            cache_key = u'type-{0}-{1}-{2}'.format(
                cls._meta.app_label,
                cls._meta.object_name,
                unicode(identifier).replace('-', '--').replace(' ', '-')
                # ^-- Memcached refuses keys with spaces
            )
            cached = cache.get(cache_key)
            if cached:
                result = cached
            elif isinstance(identifier, int):
                result = cls.objects.get(pk=identifier)
            elif isinstance(identifier, basestring):
                result = cls.objects.get(name__iexact=identifier)
            else:
                raise TypeError(
                    "Input of incorrect type (see docstring)."
                )
            cache.set(cache_key, result, 60 * 60)
        return result

    @classmethod
    def get_or_404(cls, *args, **kwargs):
        """
        Attempts to use `get` to retrieve an instance of this type,
        but returns `Http404` instead of `cls.DoesNotExist` if no
        object of the given type exists.

        Arguments are passed verbatim to `get`; see the docstring
        for `get` for parameter details.

        """
        try:
            return cls.get(*args, **kwargs)
        except cls.DoesNotExist:
            raise Http404

    ## META ##

    class Meta:
        abstract = True

    # Remember to add this
    # id = exts.primary_key_from_meta(Meta)
