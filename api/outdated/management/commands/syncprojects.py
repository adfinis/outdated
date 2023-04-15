from outdated.outdated.commands import AsyncCommand
from outdated.outdated.dependencies import ProjectSyncer
from outdated.outdated.models import Project

from asgiref.sync import sync_to_async


class Command(AsyncCommand):
    help = "Syncs all projects with their remote counterparts."

    async def _handle(self, *args, **options):
        projects = await sync_to_async(Project.objects.all())
        async for project in projects:
            try:
                self.stdout.write(f"Syncing project {project}")
                await ProjectSyncer(project).sync()
            except KeyError:  # pragma: no cover
                self.stdout.write(f"Error syncing {project}")
        self.stdout.write("Finished syncing all projects")
