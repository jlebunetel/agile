import uuid
from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import ugettext, ugettext_lazy as _
from simple_history.models import HistoricalRecords
from projects.models import BaseModel


class Product(BaseModel):
    history = HistoricalRecords()

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    point_duration = models.FloatField(
        default=1.0,
        verbose_name=_("point duration (h)"),
        help_text=_("An approximate story point duration (in hours)."),
    )

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
        return "fas fa-rocket"

    @property
    def features(self):
        from projects.models import Feature

        return Feature.objects.filter(initiative__product=self)

    @property
    def epics(self):
        from projects.models import Epic

        return Epic.objects.filter(feature__initiative__product=self)

    @property
    def issues(self):
        from projects.models import Issue

        return Issue.objects.filter(epic__feature__initiative__product=self)

    @property
    def draft_issues(self):
        from projects.models import Issue

        return Issue.objects.filter(
            epic__feature__initiative__product=self, status=Issue.DRAFT
        )

    @property
    def ready_issues(self):
        from projects.models import Issue

        return Issue.objects.filter(
            epic__feature__initiative__product=self, status=Issue.READY
        )

    @property
    def todo_issues(self):
        from projects.models import Issue

        return Issue.objects.filter(
            epic__feature__initiative__product=self, status=Issue.TO_DO
        )

    @property
    def inprogress_issues(self):
        from projects.models import Issue

        return Issue.objects.filter(
            epic__feature__initiative__product=self, status=Issue.IN_PROGRESS
        )

    @property
    def inreview_issues(self):
        from projects.models import Issue

        return Issue.objects.filter(
            epic__feature__initiative__product=self, status=Issue.IN_REVIEW
        )

    @property
    def done_issues(self):
        from projects.models import Issue

        return Issue.objects.filter(
            epic__feature__initiative__product=self, status=Issue.DONE
        )

    @property
    def blocked_issues(self):
        from projects.models import Issue

        return Issue.objects.filter(
            epic__feature__initiative__product=self, status=Issue.BLOCKED
        )

    @property
    def cancelled_issues(self):
        from projects.models import Issue

        return Issue.objects.filter(
            epic__feature__initiative__product=self, status=Issue.CANCELLED
        )

    @property
    def total_initiatives(self):
        from projects.models import Initiative

        return Initiative.objects.filter(product=self).count()

    @property
    def total_features(self):
        from projects.models import Feature

        return Feature.objects.filter(initiative__product=self).count()

    @property
    def total_epics(self):
        from projects.models import Epic

        return Epic.objects.filter(feature__initiative__product=self).count()

    @property
    def total_stories(self):
        from projects.models import Issue

        return Issue.objects.filter(
            epic__feature__initiative__product=self, label=Issue.STORY
        ).count()

    @property
    def total_bugs(self):
        from projects.models import Issue

        return Issue.objects.filter(
            epic__feature__initiative__product=self, label=Issue.BUG
        ).count()

    @property
    def total_tasks(self):
        from projects.models import Issue

        return Issue.objects.filter(
            epic__feature__initiative__product=self, label=Issue.TASK
        ).count()

    @property
    def total_story_points(self):
        from projects.models import Issue

        story_points = (
            Issue.objects.filter(epic__feature__initiative__product=self)
            .exclude(points=None)
            .aggregate(models.Sum("points"))["points__sum"]
        )

        return int(story_points) if story_points else 0
