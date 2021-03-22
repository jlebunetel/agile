from django.contrib import admin
from ordered_model.admin import OrderedTabularInline
from simple_history.admin import SimpleHistoryAdmin
from projects.admin import (
    BaseModelMixin,
    BaseInlineOrderMixin,
    FeatureInline,
)
from projects.models import Initiative


class InitiativeInline(
    BaseInlineOrderMixin,
    OrderedTabularInline,
):
    model = Initiative

    fields = (
        "id",
        "title",
        "product",
        "move_up_down_links",
    )

    ordering = ("order",)


class InitiativeAdmin(
    BaseModelMixin,
    SimpleHistoryAdmin,
):

    fields = (
        "product",
        "title",
        "description",
    )

    list_display = (
        "__str__",
        "description",
        "product",
    )

    list_filter = ("product",)

    inlines = [
        FeatureInline,
    ]


admin.site.register(Initiative, InitiativeAdmin)
