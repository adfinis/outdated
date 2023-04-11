from cProfile import Profile

from django.core.management.base import BaseCommand

from outdated.outdated.dependencies import ProjectSyncer
from outdated.outdated.models import Project


class Command(BaseCommand):
    help = "Syncs the project with the remote project"

    def add_arguments(self, parser):
        parser.add_argument("project_name", type=str)
        parser.add_argument(
            "--profile", action="store_true", help="Profile the command"
        )

    def _handle(self, *args, **options):
        project_name = options["project_name"]
        try:
            project = Project.objects.get(name__iexact=project_name)
            self.stdout.write(f"Syncing project {project}")
            ProjectSyncer(project).sync()
            self.stdout.write(f"Finished syncing {project}")
        except Project.DoesNotExist:
            self.stdout.write(f"Project {project_name} not found")

    def handle(self, *args, **options):
        if options["profile"]:  # pragma: no cover
            profiler = Profile()
            profiler.runcall(self._handle, *args, **options)
            profiler.dump_stats("syncproject.prof")
        else:
            self._handle(*args, **options)
