from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from ordered_model.models import OrderedModel
from simple_history.models import HistoricalRecords
from projects.models import BaseModel, Product


class Sprint(BaseModel):
    history = HistoricalRecords()

    # color

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="sprints",
        related_query_name="sprint",
        verbose_name=_("product"),
    )

    started_at = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("start date"),
    )

    finished_at = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("finished date"),
    )

    class Meta(BaseModel.Meta):
        verbose_name = _("sprint")
        verbose_name_plural = _("sprints")

        ordering = ["started_at"]

        constraints = [
            models.UniqueConstraint(
                fields=["title", "product"], name="sprint_title_unique_per_product"
            )
        ]

    @property
    def color(self):
        return "danger"

    @property
    def icon(self):
        return "fas fa-stopwatch"

    @property
    def parent(self):
        return self.product

    def __str__(self):
        return "[S{}] {}".format(self.id, self.title)
