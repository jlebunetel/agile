from django.apps import AppConfig
from django.utils.translation import ugettext, ugettext_lazy as _


class ProjectsConfig(AppConfig):
    name = "projects"
    verbose_name = _("Projects")

    def ready(self):
        import projects.signals
