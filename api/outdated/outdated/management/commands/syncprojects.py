from django.core.management import BaseCommand

from outdated.outdated.models import Project
from outdated.tracking import Tracker


class Command(BaseCommand):
    help = "Syncs all projects with their remote repos."

    def handle(self, *args, **options):
        [Tracker(project).sync() for project in Project.objects.all()]
        self.stdout.write("Finished syncing all projects")
