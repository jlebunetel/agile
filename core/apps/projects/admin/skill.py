from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from projects.admin import (
    BaseModelMixin,
)
from projects.models import Skill


class SkillAdmin(
    BaseModelMixin,
    SimpleHistoryAdmin,
):
    fields = (
        "title",
        "description",
    )

    list_display = (
        "__str__",
        "description",
        "changed_at",
    )


admin.site.register(Skill, SkillAdmin)
