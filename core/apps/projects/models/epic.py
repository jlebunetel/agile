from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from simple_history.models import HistoricalRecords
from projects.models import (
    BaseModel,
    Initiative,
    Feature,
    Product,
    PriorityMixin,
    ProgressMixin,
    TrustMixin,
)


class Epic(
    PriorityMixin,
    ProgressMixin,
    TrustMixin,
    BaseModel,
):
    history = HistoricalRecords()

    feature = models.ForeignKey(
        Feature,
        on_delete=models.CASCADE,
        related_name="epics",
        related_query_name="epic",
        verbose_name=_("feature"),
    )

    class Meta(BaseModel.Meta):
        verbose_name = _("epic")
        verbose_name_plural = _("epics")

        ordering = [
            "feature__initiative__product",
            "feature__initiative__order",
            "-feature__priority",
            "-priority",
            "created_at",
        ]

    @property
    def color(self):
        return "info"

    @property
    def icon(self):
        return "fas fa-book"

    @property
    def shortcut(self):
        return "#E{}".format(self.id)

    @property
    def product(self):
        return self.feature.product

    def total_story_points(self):
        points = self.issues.exclude(points=None).aggregate(models.Sum("points"))[
            "points__sum"
        ]

        return points if points else 0

    def remaining_story_points(self):
        from projects.models import Issue

        points = (
            self.issues.exclude(points=None)
            .exclude(status=Issue.DONE)
            .exclude(status=Issue.CANCELLED)
            .aggregate(models.Sum("points"))["points__sum"]
        )

        return points if points else 0

    @property
    def trust(self):
        from projects.models import Issue

        if self.issues.filter(trust=Issue.LOW) or self.issues.filter(points=None):
            return self.LOW

        if self.issues.filter(trust=Issue.MEDIUM):
            return self.MEDIUM

        return self.HIGH
