from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from ordered_model.models import OrderedModel
from simple_history.models import HistoricalRecords
from projects.models import BaseModel, Product


class Feature(BaseModel, OrderedModel):
    history = HistoricalRecords()

    # color

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="features",
        related_query_name="feature",
        verbose_name=_("product"),
    )

    order_with_respect_to = "product"

    class Meta(BaseModel.Meta, OrderedModel.Meta):
        verbose_name = _("feature")
        verbose_name_plural = _("features")

        ordering = ["order"]

        constraints = [
            models.UniqueConstraint(
                fields=["title", "product"], name="feature_title_unique_per_product"
            )
        ]

    @property
    def color(self):
        return "primary"

    @property
    def icon(self):
        return "fas fa-tag"

    @property
    def parent(self):
        return self.product

    def __str__(self):
        return "[F{}] {}".format(self.id, self.title)
