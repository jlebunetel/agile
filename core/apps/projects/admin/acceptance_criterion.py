from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin
from ordered_model.admin import OrderedTabularInline
from simple_history.admin import SimpleHistoryAdmin
from projects.admin import BaseModelMixin, BaseInlineOrderMixin
from projects.models import AcceptanceCriterion


class AcceptanceCriterionInline(BaseInlineOrderMixin, OrderedTabularInline):
    model = AcceptanceCriterion

    fields = (
        "id",
        "done",
        "title",
        "issue",
        "move_up_down_links",
    )

    ordering = ("order",)


class AcceptanceCriterionAdmin(BaseModelMixin, SimpleHistoryAdmin, OrderedModelAdmin):
    fields = (
        "issue",
        "done",
        "title",
        "description",
    )

    list_display = (
        "__str__",
        "done",
        "product",
        "initiative",
        "epic",
        "issue",
    )


admin.site.register(AcceptanceCriterion, AcceptanceCriterionAdmin)
