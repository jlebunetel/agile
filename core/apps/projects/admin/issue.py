from django.contrib import admin
from ordered_model.admin import (
    OrderedInlineModelAdminMixin,
    OrderedModelAdmin,
    OrderedTabularInline,
)
from simple_history.admin import SimpleHistoryAdmin
from projects.admin import (
    AcceptanceCriterionInline,
    BaseModelMixin,
    BaseInlineOrderMixin,
    TaskInline,
)
from projects.models import Issue


class IssueInline(BaseInlineOrderMixin, OrderedTabularInline):
    model = Issue

    fields = (
        "id",
        "label",
        "status",
        "points",
        "trust",
        "title",
        "epic",
        "feature",
        "skill",
        "sprint",
        "move_up_down_links",
    )

    ordering = ("order",)


class IssueAdmin(
    OrderedInlineModelAdminMixin, BaseModelMixin, SimpleHistoryAdmin, OrderedModelAdmin
):
    fields = (
        "epic",
        "label",
        "status",
        "points",
        "trust",
        "title",
        "description",
        "feature",
        "skill",
        "sprint",
    )

    list_display = (
        "__str__",
        "label",
        "status",
        "points",
        "trust",
        "product",
        "initiative",
        "epic",
        "feature",
        "skill",
        "sprint",
    )

    inlines = [
        AcceptanceCriterionInline,
        TaskInline,
    ]


admin.site.register(Issue, IssueAdmin)
