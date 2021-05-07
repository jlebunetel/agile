from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from projects.admin import (
    BaseModelMixin,
    BaseInlineMixin,
    EpicInline,
)
from projects.models import Feature


class FeatureInline(
    BaseInlineMixin,
    admin.TabularInline,
):
    model = Feature

    fields = (
        "id",
        "title",
        "initiative",
        "priority",
    )


class FeatureAdmin(
    BaseModelMixin,
    SimpleHistoryAdmin,
):
    fields = (
        "initiative",
        "priority",
        "title",
        "description",
    )

    list_display = (
        "__str__",
        "initiative",
        "priority",
        "description",
        "product",
        "changed_at",
    )

    inlines = [
        EpicInline,
    ]


admin.site.register(Feature, FeatureAdmin)
