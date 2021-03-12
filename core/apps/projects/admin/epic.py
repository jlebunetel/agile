from django import forms
from django.contrib import admin
from ordered_model.admin import (
    OrderedInlineModelAdminMixin,
    OrderedModelAdmin,
    OrderedTabularInline,
)
from simple_history.admin import SimpleHistoryAdmin
from projects.admin import BaseModelMixin, BaseInlineOrderMixin, IssueInline
from projects.models import Epic


class EpicInline(BaseInlineOrderMixin, OrderedTabularInline):

    model = Epic

    fields = (
        "id",
        "title",
        "initiative",
        "feature",
        "move_up_down_links",
    )

    ordering = ("order",)


class EpicAdmin(
    OrderedInlineModelAdminMixin, BaseModelMixin, SimpleHistoryAdmin, OrderedModelAdmin
):

    fields = (
        "initiative",
        "title",
        "description",
        "feature",
    )

    list_display = (
        "__str__",
        "product",
        "initiative",
        "feature",
    )

    inlines = [
        IssueInline,
    ]


admin.site.register(Epic, EpicAdmin)
