from django.conf import settings
from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from ordered_model.models import OrderedModel
from simple_history.models import HistoricalRecords
from accounts.models import get_sentinel_user
from projects.models import BaseModel, Epic, Feature, Initiative, Product, Skill, Sprint


class Issue(BaseModel, OrderedModel):
    history = HistoricalRecords()

    title = models.TextField(
        verbose_name=_("title"),
        help_text=_('As a "who", I want to "what" so that "why".'),
    )

    epic = models.ForeignKey(
        Epic,
        on_delete=models.CASCADE,
        related_name="issues",
        related_query_name="issue",
        verbose_name=_("epic"),
    )

    STORY = "STORY"
    BUG = "BUG"

    LABEL_CHOICES = [
        (STORY, _("Story")),
        (BUG, _("Bug")),
    ]

    label = models.CharField(
        max_length=10,
        choices=LABEL_CHOICES,
        default=STORY,
        verbose_name=_("label"),
    )

    DRAFT = "DRAFT"
    READY = "READY"
    TO_DO = "TO_DO"
    IN_PROGRESS = "IN_PROGRESS"
    IN_REVIEW = "IN_REVIEW"
    DONE = "DONE"
    BLOCKED = "BLOCKED"
    CANCELLED = "CANCELLED"

    STATUS_CHOICES = [
        (DRAFT, _("Draft")),
        (READY, _("Ready")),
        (TO_DO, _("To Do")),
        (IN_PROGRESS, _("In Progress")),
        (IN_REVIEW, _("In Review")),
        (DONE, _("Done")),
        (BLOCKED, _("Blocked")),
        (CANCELLED, _("Cancelled")),
    ]

    status = models.CharField(
        max_length=16,
        choices=STATUS_CHOICES,
        default=DRAFT,
        verbose_name=_("status"),
    )

    POINTS_CHOICES = [
        (None, "?"),
        (0.0, "0"),
        (0.5, "1/2"),
        (1.0, "1"),
        (2.0, "2"),
        (3.0, "3"),
        (5.0, "5"),
        (8.0, "8"),
        (13.0, "13"),
        (20.0, "20"),
        (40.0, "40"),
        (100.0, "100"),
    ]

    points = models.FloatField(
        blank=True,
        null=True,
        choices=POINTS_CHOICES,
        default=None,
        verbose_name=_("story points"),
    )

    LOW = 1
    MEDIUM = 2
    HIGH = 3

    TRUST_CHOICES = [
        (LOW, _("Low")),
        (MEDIUM, _("Medium")),
        (HIGH, _("High")),
    ]

    trust = models.SmallIntegerField(
        choices=TRUST_CHOICES,
        default=LOW,
        verbose_name=_("trust level"),
    )

    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="projects_issues",
        related_query_name="projects_issue",
        verbose_name=_("assignee"),
        help_text=_("Who works on this very story?"),
        limit_choices_to={"is_active": True},
    )

    feature = models.ForeignKey(
        Feature,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="issues",
        related_query_name="issue",
        verbose_name=_("feature"),
    )

    skill = models.ForeignKey(
        Skill,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="issues",
        related_query_name="issue",
        verbose_name=_("required skill"),
    )

    sprint = models.ForeignKey(
        Sprint,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="issues",
        related_query_name="issue",
        verbose_name=_("sprint"),
    )

    order_with_respect_to = "epic__initiative"

    class Meta(BaseModel.Meta, OrderedModel.Meta):
        verbose_name = _("issue")
        verbose_name_plural = _("issues")

        ordering = ["order"]

    @property
    def color(self):
        if self.label == self.BUG:
            return "danger"
        return "success"

    @property
    def icon(self):
        if self.label == self.BUG:
            return "fas fa-bug"
        return "fas fa-bookmark"

    @property
    def product(self):
        return self.epic.initiative.product

    @property
    def initiative(self):
        return self.epic.initiative

    @property
    def parent(self):
        return self.epic

    def __str__(self):
        return "[{}{}] {}".format(self.label[0], self.id, self.title)
