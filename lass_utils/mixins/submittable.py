"""Mixin for items that are submittable, and thus have a nullable
submission date field.

"""

from django.db import models


class SubmittableMixin(models.Model):
    """A mixin for models that represent an item that must be
    submitted in order to be used.

    """

    class Meta:
        abstract = True

    date_submitted = models.DateTimeField(
        null=True,
        auto_now_add=True,
        db_column='submitted')
