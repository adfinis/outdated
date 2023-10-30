from django.core.management.base import BaseCommand

from outdated.outdated.models import Project
from outdated.outdated.synchroniser import Synchroniser


class Command(BaseCommand):
    help = "Syncs all projects with their remote counterparts."

    def handle(self, *args, **options):
        projects = Project.objects.all()
        for project in projects:
            self.stdout.write(f"Syncing project {project}")
            Synchroniser(project).sync()
            self.stdout.write(f"Finished syncing {project}")
        self.stdout.write("Finished syncing all projects")
