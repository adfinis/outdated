from outdated.outdated.commands import AsyncCommand

from outdated.outdated.dependencies import ProjectSyncer
from outdated.outdated.models import Project


class Command(AsyncCommand):
    help = "Syncs the project with the remote project"

    def add_arguments(self, parser):
        parser.add_argument("project_name", type=str)

    async def _handle(self, *args, **options):
        project_name = options["project_name"]
        try:
            project = await Project.objects.aget(name__iexact=project_name)
            self.stdout.write(f"Syncing project {project}")
            await ProjectSyncer(project).sync()
            self.stdout.write(f"Finished syncing {project}")
        except Project.DoesNotExist:
            self.stdout.write(f"Project {project_name} not found")
