from django.core.management.base import BaseCommand

from outdated.outdated.models import Project
from outdated.outdated.synchroniser import Synchroniser


class Command(BaseCommand):
    help = "Syncs the project with the remote project"

    def add_arguments(self, parser):
        parser.add_argument("project_name", type=str)

    def handle(self, *args, **options):
        project_name = options["project_name"]
        try:
            project = Project.objects.get(name__iexact=project_name)
            self.stdout.write(f"Syncing project {project}")
            Synchroniser(project).sync()
            self.stdout.write(f"Finished syncing {project}")
        except Project.DoesNotExist:
            self.stdout.write(f"Project {project_name} not found")
