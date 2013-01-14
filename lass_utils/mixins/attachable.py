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
                   fkey=None):
        """
        Constructs a concrete implementation of this attachable model
        to provide data to a provided model.

        The attachable can either be attached to an existing model by
        passing in a foreign key field to that model as ``fkey``, or it
        can be instantiated in a stand-alone context by leaving ``fkey``
        as ``None``.

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

        # Default model name is Target-nameThis-class-name
        if model_name is None:
            model_name = ''.join((
                target_name,
                cls.__name__
            ))

        # Attach the foreign key, if present.  (If there isn't a
        # foreign key, this means we're attaching metadata to a
        # singleton class, usually.)
        if fkey:
            fields['element'] = fkey

        # Did the user specify a specific ID column?
        # If so, use that.
        if id_column:
            fields['id'] = models.AutoField(
                primary_key=True,
                db_column=id_column
            )

        # Now dynamically construct the class.
        return cls.__class__(
            model_name,
            (cls,),
            fields
        )
