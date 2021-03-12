import uuid
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from accounts.models import get_sentinel_user


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
