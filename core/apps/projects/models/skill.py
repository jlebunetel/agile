from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from ordered_model.models import OrderedModel
from simple_history.models import HistoricalRecords
from projects.models import BaseModel, Product


class Skill(BaseModel, OrderedModel):
    history = HistoricalRecords()

    # color

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="skills",
        related_query_name="skill",
        verbose_name=_("product"),
    )

    order_with_respect_to = "product"

    class Meta(BaseModel.Meta, OrderedModel.Meta):
        verbose_name = _("skill")
        verbose_name_plural = _("skills")

        ordering = ["order"]

        constraints = [
            models.UniqueConstraint(
                fields=["title", "product"], name="skill_title_unique_per_product"
            )
        ]

    @property
    def color(self):
        return "link"

    @property
    def icon(self):
        return "fas fa-user-tag"

    @property
    def parent(self):
        return self.product

    def __str__(self):
        return "[S{}] {}".format(self.id, self.title)
