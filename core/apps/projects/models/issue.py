from django.conf import settings
from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from simple_history.models import HistoricalRecords
from accounts.models import get_sentinel_user
from projects.models import (
    BaseModel,
    Epic,
    Skill,
    PriorityMixin,
)


class Issue(
    PriorityMixin,
    BaseModel,
):
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
    TASK = "TASK"

    LABEL_CHOICES = [
        (STORY, _("Story")),
        (BUG, _("Bug")),
        (TASK, _("Task")),
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
        help_text=_(
            """Draft: <br>
            Ready: L'estimation est réaliste, les skills sont identifiées, l'issue est prête à être réalisée.<br>
            To Do: Selectionnée pour le prochain sprint.<br>
            In Progress: <br>
            In Review: <br>
            Done: <br>
            Blocked: Un problème empêche la réalisation de l'issue.<br>
            Cancelled: """
        ),
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
        help_text=_("How realistic is the story point estimate?"),
    )

    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="assigned_issues",
        related_query_name="assigned_issue",
        verbose_name=_("assignee"),
        help_text=_("Who works on this very story?"),
        limit_choices_to={"is_active": True},
    )

    skills = models.ManyToManyField(
        Skill,
        blank=True,
        related_name="issues",
        related_query_name="issue",
        verbose_name=_("required skills"),
        help_text=_("Main skills required to achieve this issue."),
    )

    class Meta(BaseModel.Meta):
        verbose_name = _("issue")
        verbose_name_plural = _("issues")

        ordering = [
            "epic__feature__initiative__product",
            "epic__feature__initiative__order",
            "-epic__feature__priority",
            "-epic__priority",
            "-priority",
            "created_at",
        ]

    @property
    def color(self):
        if self.status == self.BLOCKED:
            return "danger"

        if self.status in [self.DONE, self.CANCELLED]:
            return "grey-lighter"

        return "grey"

    @property
    def icon(self):
        if self.label == self.BUG:
            return "fas fa-bug"

        elif self.label == self.TASK:
            return "fas fa-check-square"

        return "fas fa-bookmark"

    @property
    def shortcut(self):
        return "{}{}".format(self.label[0].upper(), self.id)

    @property
    def product(self):
        return self.epic.product

    def get_trust_color(self):
        if self.points == None:
            return "danger"

        if self.trust == self.HIGH:
            return "light"

        elif self.trust == self.MEDIUM:
            return "warning"

        else:
            return "danger"

    def get_status_color(self):
        if self.status == self.DRAFT:
            return "warning"

        if self.status == self.READY:
            return "success"

        if self.status == self.TO_DO:
            return "info"

        if self.status == self.IN_PROGRESS:
            return "warning"

        if self.status == self.IN_REVIEW:
            return "success"

        if self.status == self.DONE:
            return "light"

        if self.status == self.BLOCKED:
            return "danger"

        if self.status == self.CANCELLED:
            return "light"

        return "light"

    def duration(self):
        if self.points == None:
            return "?"

        return "≈ {0:2.0f}h{1:02.0f}".format(
            *divmod(self.product.point_duration * self.points * 60, 60)
        )
