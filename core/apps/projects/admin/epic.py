from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from projects.admin import (
    BaseModelMixin,
    BaseInlineMixin,
    IssueInline,
)
from projects.models import Epic


class EpicInline(
    BaseInlineMixin,
    admin.TabularInline,
):

    model = Epic

    fields = (
        "id",
        "feature",
        "priority",
        "title",
    )


class EpicAdmin(
    BaseModelMixin,
    SimpleHistoryAdmin,
):

    fields = (
        "feature",
        "priority",
        "title",
        "description",
    )

    list_display = (
        "__str__",
        "feature",
        "priority",
        "description",
        "product",
    )

    inlines = [
        IssueInline,
    ]


admin.site.register(Epic, EpicAdmin)
