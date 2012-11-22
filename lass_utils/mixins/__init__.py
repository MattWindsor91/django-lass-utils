"""
Mixins
======

Anything that adds functionality, or a common interface, to a
model without necessarily specifying anything about the context of
the model is termed a *mixin*.

Many of these are in actual fact abstract models, which means that
they often cannot be combined in a class that also inherits directly
from `django.models.Model`.

.. automodule:: lass_utils.mixins.submittable
    :deprecated:
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: lass_utils.mixins.date_range
    :deprecated:
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: lass_utils.mixins.effective_range
    :deprecated:
    :members:
    :undoc-members:
    :show-inheritance:

"""
from lass_utils.mixins.submittable import SubmittableMixin
from lass_utils.mixins.date_range import DateRangeMixin
from lass_utils.mixins.effective_range import EffectiveRangeMixin
