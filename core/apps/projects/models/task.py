from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from ordered_model.models import OrderedModel
from simple_history.models import HistoricalRecords
from projects.models import BaseModel, Issue


class Task(BaseModel, OrderedModel):
    history = HistoricalRecords()

    issue = models.ForeignKey(
        Issue,
        on_delete=models.CASCADE,
        related_name="tasks",
        related_query_name="task",
        verbose_name=_("issue"),
    )

    done = models.BooleanField(
        default=False,
        verbose_name=_("done"),
    )

    order_with_respect_to = "issue"

    class Meta(BaseModel.Meta, OrderedModel.Meta):
        verbose_name = _("task")
        verbose_name_plural = _("tasks")

        ordering = ["order"]

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
    def parent(self):
        return self.issue

    @property
    def product(self):
        return self.parent.product

    @property
    def initiative(self):
        return self.parent.initiative

    @property
    def epic(self):
        return self.parent.epic

    def __str__(self):
        return "[T{}] {}".format(self.id, self.title)
