from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from ordered_model.models import OrderedModel
from simple_history.models import HistoricalRecords
from projects.models import BaseModel, Issue


class Subtask(BaseModel, OrderedModel):
    history = HistoricalRecords()

    issue = models.ForeignKey(
        Issue,
        on_delete=models.CASCADE,
        related_name="subtasks",
        related_query_name="subtask",
        verbose_name=_("issue"),
    )

    done = models.BooleanField(
        default=False,
        verbose_name=_("done"),
    )

    order_with_respect_to = "issue"

    class Meta(BaseModel.Meta, OrderedModel.Meta):
        verbose_name = _("subtask")
        verbose_name_plural = _("subtasks")

        ordering = [
            "issue",
            "order",
        ]

    @property
    def color(self):
        if self.done:
            return "grey"
        return "dark"

    @property
    def icon(self):
        if self.done:
            return "far fa-check-square"
        return "far fa-square"

    @property
    def product(self):
        return self.issue.product

    @property
    def shortcut(self):
        return "#ST{}".format(self.id)
