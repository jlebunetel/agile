from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from ordered_model.models import OrderedModel
from simple_history.models import HistoricalRecords
from projects.models import BaseModel, Initiative, Feature, Product


class Epic(BaseModel, OrderedModel):
    history = HistoricalRecords()

    initiative = models.ForeignKey(
        Initiative,
        on_delete=models.CASCADE,
        related_name="epics",
        related_query_name="epic",
        verbose_name=_("initiative"),
    )

    feature = models.ForeignKey(
        Feature,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="epics",
        related_query_name="epic",
        verbose_name=_("feature"),
    )

    order_with_respect_to = "initiative__product"

    class Meta(BaseModel.Meta, OrderedModel.Meta):
        verbose_name = _("epic")
        verbose_name_plural = _("epics")

        ordering = ["order"]

        constraints = [
            models.UniqueConstraint(
                fields=["title", "initiative"], name="epic_title_unique_per_initiative"
            )
        ]

    @property
    def color(self):
        return "info"

    @property
    def icon(self):
        return "fas fa-book"

    @property
    def product(self):
        return self.initiative.product

    @property
    def parent(self):
        return self.initiative

    @property
    def is_auto(self):
        return self.title == self.parent.title

    def __str__(self):
        return "[E{}] {}".format(self.id, self.title)
