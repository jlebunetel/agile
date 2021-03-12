from django.contrib import admin
from ordered_model.admin import (
    OrderedInlineModelAdminMixin,
    OrderedModelAdmin,
    OrderedTabularInline,
)
from simple_history.admin import SimpleHistoryAdmin
from projects.admin import BaseModelMixin, BaseInlineOrderMixin, EpicInline
from projects.models import Initiative


class InitiativeInline(BaseInlineOrderMixin, OrderedTabularInline):
    model = Initiative

    fields = (
        "id",
        "title",
        "product",
        "move_up_down_links",
    )

    ordering = ("order",)


class InitiativeAdmin(
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
    )

    inlines = [
        EpicInline,
    ]


admin.site.register(Initiative, InitiativeAdmin)
