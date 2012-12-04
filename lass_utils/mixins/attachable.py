"""
This module contains the :class:`AttachableMixin` mixin for defining
models that attach optional information onto other models in a many
to one form.

"""

from django.db import models


class AttachableMixin(object):
    """
    Interface for "attachable" models.

    An *attachable* model is one that contains optional data that can be
    "attached" onto another model via subclassing.  It is a pattern
    used in LASS primarily for metadata, such as the metadata and credits
    systems.

    Subclasses used to attach the model to other models are created via
    the :meth:`AttachableMixin.make_model` class factory method.  By
    convention, the foreign key to the attached model is stored in
    :attr:`AttachableMixin.element`.

    """

    @classmethod
    def make_model(cls,
                   target_class,
                   app=None,
                   model_name=None,
                   table=None,
                   id_column=None,
                   fkey_column=None,
                   help_text=None):
        """
        Constructs a concrete implementation of this attachable model
        to provide data to a provided model.

        """
        if isinstance(target_class, basestring):
            # We got a string in, which is hopefully a model name.
            # This means the target name and the target are equal.
            target_name = target_class
        else:
            # We got something that we hope is a class object in.
            # Its name is just the __name__ param.
            target_name = target_class.__name__

        # The 'fields' dict will contain the fields that we're
        # adding on top of cls for the metadata class we're building.
        fields = {'__module__': __name__}

        # Make a meta class with the correct database table, app label
        # and 'abstract' switched on.
        class Meta(cls.Meta):
            abstract = False
            if table:
                db_table = table
            if app:
                app_label = app
        fields['Meta'] = Meta

        # Default model name is Target-nameThis-type-ofMetadata
        if model_name is None:
            model_name = ''.join((
                target_name,
                cls.__name__
            ))

        # Make the foreign key pointing to the element.
        # - Let's make the dict of arguments to the foreign key class.
        fkey_kwargs = {}
        # - Did the user specify a foreign key?
        if fkey_column:
            fkey_kwargs['db_column'] = fkey_column
        # - Now we can have a foreign key...
        fields['element'] = models.ForeignKey(
            target_class,
            **fkey_kwargs
        )

        # Now dynamically construct the class.
        return cls.__class__(
            model_name,
            (cls,),
            fields
        )
