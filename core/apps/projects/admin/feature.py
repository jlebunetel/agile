from django.contrib import admin
from ordered_model.admin import (
    OrderedInlineModelAdminMixin,
    OrderedModelAdmin,
    OrderedTabularInline,
)
from simple_history.admin import SimpleHistoryAdmin
from projects.admin import BaseModelMixin, BaseInlineOrderMixin, EpicInline, IssueInline
from projects.models import Feature


class FeatureInline(BaseInlineOrderMixin, OrderedTabularInline):
    model = Feature

    fields = (
        "id",
        "title",
        "product",
        "move_up_down_links",
    )

    readonly_fields = ("move_up_down_links",)

    ordering = ("order",)


class FeatureAdmin(
    OrderedInlineModelAdminMixin, BaseModelMixin, SimpleHistoryAdmin, OrderedModelAdmin
):
    fields = (
        "product",
        "title",
        "description",
    )

    list_display = (
        "__str__",
        "product",
        "description",
    )

    inlines = [
        EpicInline,
        IssueInline,
    ]


admin.site.register(Feature, FeatureAdmin)
