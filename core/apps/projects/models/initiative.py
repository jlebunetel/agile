from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from ordered_model.models import OrderedModel
from simple_history.models import HistoricalRecords
from projects.models import (
    BaseModel,
    Product,
    ProgressMixin,
    TrustMixin,
)


class Initiative(
    ProgressMixin,
    TrustMixin,
    BaseModel,
    OrderedModel,
):
    history = HistoricalRecords()

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="initiatives",
        related_query_name="initiative",
        verbose_name=_("product"),
    )

    order_with_respect_to = "product"

    class Meta(BaseModel.Meta, OrderedModel.Meta):
        verbose_name = _("initiative")
        verbose_name_plural = _("initiatives")

        ordering = ["order"]

        constraints = [
            models.UniqueConstraint(
                fields=["title", "product"], name="initiative_title_unique_per_product"
            )
        ]

    @property
    def color(self):
        return "link"

    @property
    def icon(self):
        return "fas fa-cogs"

    @property
    def shortcut(self):
        return "#I{}".format(self.id)

    def total_story_points(self):
        points = 0

        for feature in self.features.all():
            points += feature.total_story_points()

        return points

    def remaining_story_points(self):
        points = 0

        for feature in self.features.all():
            points += feature.remaining_story_points()

        return points

    @property
    def trust(self):
        from projects.models import Feature

        for feature in self.features.all():
            if feature.trust == Feature.LOW:
                return self.LOW

        for feature in self.features.all():
            if feature.trust == Feature.MEDIUM:
                return self.MEDIUM

        return self.HIGH
