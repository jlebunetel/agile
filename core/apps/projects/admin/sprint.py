from django.contrib import admin
from ordered_model.admin import (
    OrderedInlineModelAdminMixin,
    OrderedModelAdmin,
    OrderedTabularInline,
)
from simple_history.admin import SimpleHistoryAdmin
from projects.admin import BaseModelMixin, BaseInlineMixin, IssueInline
from projects.models import Sprint


class SprintInline(admin.TabularInline):
    model = Sprint

    fields = (
        "id",
        "title",
        "product",
        "started_at",
        "finished_at",
        # "move_up_down_links",
    )

    # readonly_fields = ("move_up_down_links",)

    # ordering = ("order",)


class SprintAdmin(
    OrderedInlineModelAdminMixin, BaseModelMixin, SimpleHistoryAdmin, OrderedModelAdmin
):
    fields = (
        "product",
        "title",
        "description",
        "started_at",
        "finished_at",
    )

    list_display = (
        "__str__",
        "product",
        "description",
        "started_at",
        "finished_at",
    )

    inlines = [
        IssueInline,
    ]


admin.site.register(Sprint, SprintAdmin)
