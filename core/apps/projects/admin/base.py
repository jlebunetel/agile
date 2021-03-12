from django import forms
from django.contrib import admin
from django.contrib.sites.models import Site
from django.utils.translation import ugettext, ugettext_lazy as _
from projects.models import BaseModel


class BaseInlineFormSet(forms.BaseInlineFormSet):
    """Permets de retrouver l'objet parent à partir d'un form inline"""

    def get_form_kwargs(self, index):
        kwargs = super(BaseInlineFormSet, self).get_form_kwargs(index)
        kwargs.update({"parent": self.instance})
        return kwargs


class BaseInlineAdminForm(forms.ModelForm):
    """Permets de :
    - limiter la liste des « features » selectionnables dans les forms inlines à celles liées au Product.
      attention : pour le form principal, on fait la même chose dans BaseAdminForm
    - rendre non éditable les objets enfants créé par défault (c'est à dire qui on le même title)
      attention : pour le form principal, on utilise get_readonly_fields()
    """

    def __init__(self, *args, parent=None, **kwargs):
        super(BaseInlineAdminForm, self).__init__(*args, **kwargs)

        if self.instance and self.instance.id:
            if self.instance.title == parent.title:
                if "title" in self.fields:
                    self.fields["title"].widget.attrs["readonly"] = "readonly"

                if "description" in self.fields:
                    self.fields["description"].widget.attrs["readonly"] = "readonly"

                if "feature" in self.fields:
                    self.fields["feature"].disabled = True

                if "skill" in self.fields:
                    self.fields["skill"].disabled = True

                if "sprint" in self.fields:
                    self.fields["sprint"].disabled = True

        if hasattr(parent, "product"):
            if "feature" in self.fields:
                self.fields["feature"].queryset = parent.product.features.all()

            if "skill" in self.fields:
                self.fields["skill"].queryset = parent.product.skills.all()

            if "sprint" in self.fields:
                self.fields["sprint"].queryset = parent.product.sprints.all()

            if "initiative" in self.fields:
                self.fields["initiative"].queryset = parent.product.initiatives.all()

            if "epic" in self.fields:
                self.fields["epic"].queryset = parent.product.epics.all()


class BaseInlineMixin(object):
    form = BaseInlineAdminForm
    formset = BaseInlineFormSet

    extra = 1

    readonly_fields = ("id",)


class BaseInlineOrderMixin(object):
    form = BaseInlineAdminForm
    formset = BaseInlineFormSet

    extra = 1

    show_change_link = True

    readonly_fields = (
        "id",
        "move_up_down_links",
    )


class BaseAdminForm(forms.ModelForm):
    """Permets de limiter la liste des « features » et des « initiatives » selectionnables dans les forms à celles liées au Product."""

    def __init__(self, *args, **kwargs):
        super(BaseAdminForm, self).__init__(*args, **kwargs)

        if self.instance.id and hasattr(self.instance, "product"):
            if "feature" in self.fields:
                self.fields["feature"].queryset = self.instance.product.features.all()

            if "skill" in self.fields:
                self.fields["skill"].queryset = self.instance.product.skills.all()

            if "sprint" in self.fields:
                self.fields["sprint"].queryset = self.instance.product.sprints.all()

            if "initiative" in self.fields:
                self.fields[
                    "initiative"
                ].queryset = self.instance.product.initiatives.all()

            if "epic" in self.fields:
                self.fields["epic"].queryset = self.instance.product.epics.all()

            if "issue" in self.fields:
                self.fields["issue"].queryset = self.instance.product.issues.all()


class BaseModelMixin(object):
    form = BaseAdminForm

    def get_fieldsets(self, request, obj=None):
        fieldsets_base = (
            (
                _("generic fields"),
                {
                    "classes": ("collapse",),
                    "fields": (
                        "id",
                        "created_at",
                        "created_by",
                        "changed_at",
                        "changed_by",
                        "owner",
                    ),
                },
            ),
        )
        if self.fields:
            return fieldsets_base + ((_("specific fields"), {"fields": self.fields}),)
        return fieldsets_base

    def get_readonly_fields(self, request, obj=None):

        readonly_fields_base = (
            "id",
            "created_at",
            "created_by",
            "changed_at",
            "changed_by",
        )

        if obj:
            readonly_fields_parent = ("owner", "product")

            # rendre non éditable les objets enfants créés par défault:
            if hasattr(obj, "parent"):
                if obj.title == obj.parent.title:
                    readonly_fields_parent += (
                        "title",
                        "description",
                        "feature",
                        "skill",
                        "sprint",
                    )

            return self.readonly_fields + readonly_fields_base + readonly_fields_parent

        else:
            return (
                self.readonly_fields
                + readonly_fields_base
                + ("owner", "feature", "skill", "sprint")
            )

    def get_list_display(self, request):
        list_display_base = ()
        return self.list_display + list_display_base

    def get_search_fields(self, request):
        return self.search_fields + ("id",)

    def get_inline_instances(self, request, obj=None):
        if obj:
            return [inline(self.model, self.admin_site) for inline in self.inlines]
        else:
            return []

    def save_model(self, request, obj, form, change):
        if not change:
            obj.owner = request.user
        super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        """Méthode appellée lorsqu'un objet est créé via un formulaire inline"""

        for formset in formsets:

            if issubclass(formset.model, BaseModel):
                instances = formset.save(commit=False)

                for added_obj in formset.new_objects:
                    added_obj.owner = request.user

                for deleted_obj in formset.deleted_objects:
                    pass

        super(BaseModelMixin, self).save_related(request, form, formsets, change)


class ReadOnlyModelMixin(object):
    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
