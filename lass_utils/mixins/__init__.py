"""
The `lass-utils` module contains many mixins for adding common
patterns, both pertinent to the metadata subsystem and not, to
existing models.

Many of these mixins are abstract models that add in new fields on
existing models; you may need to remove direct inheritance from
`django.db.models.Model` to make these work.

"""
from metadata.mixins.submittable import SubmittableMixin
from metadata.mixins.date_range import DateRangeMixin
from metadata.mixins.effective_range import EffectiveRangeMixin
