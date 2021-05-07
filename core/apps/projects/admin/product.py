from django.contrib import admin
from ordered_model.admin import OrderedInlineModelAdminMixin
from simple_history.admin import SimpleHistoryAdmin
from projects.admin import (
    BaseModelMixin,
    InitiativeInline,
)
from projects.models import Product


class ProductAdmin(
    OrderedInlineModelAdminMixin,
    BaseModelMixin,
    SimpleHistoryAdmin,
):
    fields = (
        "title",
        "description",
        "point_duration",
    )

    list_display = (
        "__str__",
        "description",
        "point_duration",
        "changed_at",
    )

    inlines = [
        InitiativeInline,
    ]


admin.site.register(Product, ProductAdmin)
