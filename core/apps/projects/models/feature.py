from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from simple_history.models import HistoricalRecords
from projects.models import (
    BaseModel,
    Initiative,
    PriorityMixin,
    ProgressMixin,
    TrustMixin,
)


class Feature(
    PriorityMixin,
    ProgressMixin,
    TrustMixin,
    BaseModel,
):
    history = HistoricalRecords()

    initiative = models.ForeignKey(
        Initiative,
        on_delete=models.CASCADE,
        related_name="features",
        related_query_name="feature",
        verbose_name=_("initiative"),
    )

    class Meta(BaseModel.Meta):
        verbose_name = _("feature")
        verbose_name_plural = _("features")

        ordering = [
            "initiative__product",
            "initiative__order",
            "-priority",
            "created_at",
        ]

    @property
    def color(self):
        return "primary"

    @property
    def icon(self):
        return "fas fa-cog"

    @property
    def shortcut(self):
        return "F{}".format(self.id)

    @property
    def product(self):
        return self.initiative.product

    def total_story_points(self):
        points = 0

        for epic in self.epics.all():
            points += epic.total_story_points()

        return points

    def remaining_story_points(self):
        points = 0

        for epic in self.epics.all():
            points += epic.remaining_story_points()

        return points

    @property
    def trust(self):
        from projects.models import Epic

        for epic in self.epics.all():
            if epic.trust == Epic.LOW:
                return self.LOW

        for epic in self.epics.all():
            if epic.trust == Epic.MEDIUM:
                return self.MEDIUM

        return self.HIGH
