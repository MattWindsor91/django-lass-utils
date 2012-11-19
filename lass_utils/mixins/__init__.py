"""
The `lass-utils` module contains many mixins for adding common
patterns, both pertinent to the lass_utils subsystem and not, to
existing models.

Many of these mixins are abstract models that add in new fields on
existing models; you may need to remove direct inheritance from
`django.db.models.Model` to make these work.

"""
from lass_utils.mixins.submittable import SubmittableMixin
from lass_utils.mixins.date_range import DateRangeMixin
from lass_utils.mixins.effective_range import EffectiveRangeMixin
