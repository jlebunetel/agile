from django.contrib import admin
from ordered_model.admin import (
    OrderedInlineModelAdminMixin,
    OrderedModelAdmin,
    OrderedTabularInline,
)
from simple_history.admin import SimpleHistoryAdmin
from projects.admin import BaseModelMixin, BaseInlineOrderMixin, IssueInline
from projects.models import Skill


class SkillInline(BaseInlineOrderMixin, OrderedTabularInline):
    model = Skill

    fields = (
        "id",
        "title",
        "product",
        "move_up_down_links",
    )

    readonly_fields = ("move_up_down_links",)

    ordering = ("order",)


class SkillAdmin(
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
        IssueInline,
    ]


admin.site.register(Skill, SkillAdmin)
