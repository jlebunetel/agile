import markdown
import uuid
from django.conf import settings
from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import ugettext, ugettext_lazy as _
from accounts.models import get_sentinel_user


class PriorityMixin(models.Model):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

    PRIORITY_CHOICES = [
        (HIGH, _("High")),
        (MEDIUM, _("Medium")),
        (LOW, _("Low")),
    ]

    priority = models.SmallIntegerField(
        choices=PRIORITY_CHOICES,
        default=MEDIUM,
        verbose_name=_("priority"),
        help_text=_("Priority relating to the parent object."),
    )

    class Meta:
        abstract = True

    @property
    def shortcut(self):
        return "#?{}".format(self.id)

    def __str__(self):
        return "[{}] {}".format(self.shortcut, self.title)

    def get_priority_color(self):
        if self.priority == self.HIGH:
            return "danger"
        elif self.priority == self.MEDIUM:
            return "warning"
        else:
            return "success"

    def get_priority_icon(self):
        if self.priority == self.HIGH:
            return "fas fa-angle-double-up"
        elif self.priority == self.MEDIUM:
            return "fas fa-angle-up"
        else:
            return "fas fa-angle-down"


class ProgressMixin(models.Model):
    class Meta:
        abstract = True

    def get_points_display(self):
        total = self.total_story_points()
        remaining = self.remaining_story_points()
        return "{} / {}".format(total - remaining, total)

    def progress(self):
        """Returns progress from 0 to 100 according to child issue states."""
        total = self.total_story_points()
        remaining = self.remaining_story_points()
        if not total:
            return 0
        return int(100 * (total - remaining) / total)


class TrustMixin(models.Model):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

    TRUST_CHOICES = [
        (LOW, _("Low")),
        (MEDIUM, _("Medium")),
        (HIGH, _("High")),
    ]

    class Meta:
        abstract = True

    def get_trust_display(self):
        trust = self.trust
        for t in self.TRUST_CHOICES:
            if trust == t[0]:
                return t[1]
        return self.LOW

    def get_trust_color(self):
        total = self.total_story_points()
        if not total:
            return "warning"
        if self.trust == self.HIGH:
            return "light"
        elif self.trust == self.MEDIUM:
            return "warning"
        else:
            return "danger"


class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET(
            get_sentinel_user
        ),  # if the related user is deleted, sets the creator to the "deleted" user!
        related_name="%(app_label)s_%(class)ss_as_owner",
        related_query_name="%(app_label)s_%(class)s_as_owner",
        verbose_name=_("owner"),
        help_text=_("Owner of this very object."),
        limit_choices_to={"is_active": True},
    )

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("creation date")
    )

    changed_at = models.DateTimeField(auto_now=True, verbose_name=_("update date"))

    title = models.CharField(
        max_length=255,
        verbose_name=_("title"),
    )

    description = models.TextField(
        blank=True,
        verbose_name=_("description"),
        help_text=_("Tip: You can use Markdown's syntax!"),
    )

    class Meta:
        abstract = True
        ordering = ["-changed_at"]

    def __str__(self):
        return self.title

    def get_created_by(self):
        return self.history.earliest().history_user

    get_created_by.short_description = _("created by")
    created_by = property(get_created_by)

    def get_changed_by(self):
        return self.history.latest().history_user

    get_changed_by.short_description = _("changed by")
    changed_by = property(get_changed_by)

    def get_edit_url(self):
        return reverse_lazy(
            "admin:%s_%s_change" % (self._meta.app_label, self._meta.model_name),
            args=(self.id,),
        )

    @property
    def description_html(self):
        return markdown.markdown(self.description)
