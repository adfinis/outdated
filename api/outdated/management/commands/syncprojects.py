from django.core.management.base import BaseCommand

from outdated.outdated.dependencies import ProjectSyncer
from outdated.outdated.models import Project


class Command(BaseCommand):
    help = "Syncs all projects with their remote counterparts."

    def handle(self, *args, **options):
        projects = Project.objects.all()
        for project in projects:
            try:
                self.stdout.write(f"Syncing project {project}")
                ProjectSyncer(project).sync()
            except KeyError:  # pragma: no cover
                self.stdout.write(f"Error syncing {project}")
        self.stdout.write("Finished syncing all projects")
