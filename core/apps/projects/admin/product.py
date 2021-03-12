from django.contrib import admin
from ordered_model.admin import OrderedInlineModelAdminMixin
from simple_history.admin import SimpleHistoryAdmin
from projects.admin import (
    BaseModelMixin,
    InitiativeInline,
    FeatureInline,
    SkillInline,
    SprintInline,
)
from projects.models import Product


class ProductAdmin(OrderedInlineModelAdminMixin, BaseModelMixin, SimpleHistoryAdmin):
    fields = (
        "title",
        "description",
    )

    readonly_fields = ("owner",)

    list_display = ("__str__",)

    inlines = [
        InitiativeInline,
        FeatureInline,
        SkillInline,
        SprintInline,
    ]


admin.site.register(Product, ProductAdmin)
