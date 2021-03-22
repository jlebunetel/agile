from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from simple_history.models import HistoricalRecords
from projects.models import BaseModel, Product


class Skill(BaseModel):
    history = HistoricalRecords()

    class Meta(BaseModel.Meta):
        verbose_name = _("skill")
        verbose_name_plural = _("skills")

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "title",
                ],
                name="skill_title_unique_per_app",
            )
        ]

    @property
    def color(self):
        return "link"

    @property
    def icon(self):
        return "fas fa-user-tag"
