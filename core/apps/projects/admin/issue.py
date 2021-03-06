from django import forms
from django.contrib import admin
from django.utils.translation import ugettext, ugettext_lazy as _
from ordered_model.admin import OrderedInlineModelAdminMixin
from simple_history.admin import SimpleHistoryAdmin
from projects.admin import (
    BaseAdminForm,
    BaseInlineMixin,
    BaseModelMixin,
    SubtaskInline,
)
from projects.models import Issue


class IssueAdminCleanMixin(object):
    def clean(object):
        cleaned_data = super().clean()
        # current_status = object.instance.status
        status = cleaned_data.get("status")

        points = cleaned_data.get("points")
        if points == None:
            points = object.instance.points

        trust = cleaned_data.get("trust")
        if not trust:
            trust = object.instance.trust

        if (
            status
            not in [
                object.instance.DRAFT,
                object.instance.CANCELLED,
            ]
            and (points == None or trust != object.instance.HIGH)
        ):
            raise forms.ValidationError(
                _("Please specify points and trust to High before changing the status.")
            )

        return cleaned_data


class IssueInlineAdminForm(IssueAdminCleanMixin, forms.ModelForm):
    def __init__(self, *args, parent=None, **kwargs):
        super(IssueInlineAdminForm, self).__init__(*args, **kwargs)

        if self.instance and self.instance.id:
            if "status" in self.fields:
                if self.instance.status != self.instance.DRAFT:
                    self.fields["points"].disabled = True
                    self.fields["trust"].disabled = True
                    self.fields["skills"].disabled = True

        """
        if hasattr(parent, "product"):
            if "sprint" in self.fields:
                self.fields["sprint"].queryset = parent.product.sprints.all()
        """


class IssueAdminForm(IssueAdminCleanMixin, BaseAdminForm):
    pass


class IssueInline(
    BaseInlineMixin,
    admin.TabularInline,
):
    form = IssueInlineAdminForm

    model = Issue

    fields = (
        "id",
        "label",
        "status",
        "points",
        "trust",
        "skills",
        "title",
        "epic",
        "priority",
    )


class IssueAdmin(
    OrderedInlineModelAdminMixin,
    BaseModelMixin,
    SimpleHistoryAdmin,
):

    form = IssueAdminForm

    fields = (
        "epic",
        "priority",
        "label",
        "status",
        "points",
        "trust",
        "skills",
        "title",
        "description",
    )

    list_display = (
        "__str__",
        # "label",
        "status",
        "points",
        "duration",
        "trust",
        "priority",
        "epic",
        "product",
        "changed_at",
    )

    list_filter = (
        "status",
        "label",
        "priority",
    )

    inlines = [
        SubtaskInline,
    ]

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = ()

        if obj:
            if hasattr(obj, "status"):
                if obj.status != obj.DRAFT:
                    readonly_fields += (
                        "points",
                        "trust",
                        "skills",
                    )

        return self.readonly_fields_base + readonly_fields


admin.site.register(Issue, IssueAdmin)
