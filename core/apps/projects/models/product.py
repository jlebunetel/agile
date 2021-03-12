import uuid
from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import ugettext, ugettext_lazy as _
from simple_history.models import HistoricalRecords
from projects.models import BaseModel


class Product(BaseModel):
    history = HistoricalRecords()

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta(BaseModel.Meta):
        verbose_name = _("product")
        verbose_name_plural = _("products")

    def get_absolute_url(self):
        return reverse_lazy("projects:product-detail", args=[str(self.id)])

    @property
    def color(self):
        return "primary"

    @property
    def icon(self):
        return "fas fa-paper-plane"

    @property
    def epics(self):
        from projects.models import Epic

        return Epic.objects.filter(initiative__product=self)

    @property
    def issues(self):
        from projects.models import Issue

        return Issue.objects.filter(epic__initiative__product=self)

    @property
    def total_features(self):
        from projects.models import Feature

        return Feature.objects.filter(product=self).count()

    @property
    def total_skills(self):
        from projects.models import Skill

        return Skill.objects.filter(product=self).count()

    @property
    def total_initiatives(self):
        from projects.models import Initiative

        return Initiative.objects.filter(product=self).count() - 1

    @property
    def total_epics(self):
        from projects.models import Epic

        return Epic.objects.filter(initiative__product=self).count() - (
            self.total_initiatives + 1
        )

    @property
    def total_stories(self):
        from projects.models import Issue

        return Issue.objects.filter(
            epic__initiative__product=self, label=Issue.STORY
        ).count()

    @property
    def total_bugs(self):
        from projects.models import Issue

        return Issue.objects.filter(
            epic__initiative__product=self, label=Issue.BUG
        ).count()

    @property
    def total_story_points(self):
        from projects.models import Issue

        return int(
            Issue.objects.filter(epic__initiative__product=self)
            .exclude(points=None)
            .aggregate(models.Sum("points"))["points__sum"]
        )

        return (
            Issue.objects.filter(epic__initiative__product=self)
            .exclude(points=None)
            .annotate(total=models.Sum("points"))
            .values("total")
        )
