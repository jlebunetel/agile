from django.contrib import admin
from ordered_model.admin import OrderedTabularInline
from simple_history.admin import SimpleHistoryAdmin
from projects.admin import BaseModelMixin, BaseInlineOrderMixin
from projects.models import Subtask


class SubtaskInline(
    BaseInlineOrderMixin,
    OrderedTabularInline,
):
    model = Subtask

    fields = (
        "id",
        "done",
        "title",
        "issue",
        "move_up_down_links",
    )

    ordering = ("order",)


class SubtaskAdmin(
    BaseModelMixin,
    SimpleHistoryAdmin,
):
    fields = (
        "issue",
        "done",
        "title",
        "description",
    )

    list_display = (
        "__str__",
        "done",
        "issue",
        "product",
    )


admin.site.register(Subtask, SubtaskAdmin)
