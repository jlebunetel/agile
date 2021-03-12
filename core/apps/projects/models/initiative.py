from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from ordered_model.models import OrderedModel
from simple_history.models import HistoricalRecords
from projects.models import BaseModel, Product


class Initiative(BaseModel, OrderedModel):
    history = HistoricalRecords()

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="initiatives",
        related_query_name="initiative",
        verbose_name=_("product"),
    )

    # color

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
        return "fas fa-cloud"

    @property
    def parent(self):
        return self.product

    @property
    def is_auto(self):
        return self.title == self.parent.title

    @property
    def issues(self):
        from projects.models import Issue

        return Issue.objects.filter(epic__initiative=self)

    def __str__(self):
        return "[I{}] {}".format(self.id, self.title)
