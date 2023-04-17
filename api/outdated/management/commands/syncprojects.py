from asyncio import gather

from outdated.outdated.commands import AsyncCommand
from outdated.outdated.dependencies import ProjectSyncer
from outdated.outdated.models import Project


class Command(AsyncCommand):
    help = "Syncs all projects with their remote counterparts."

    async def _handle(self, *args, **options):
        projects = Project.objects.all()
        project_tasks = [ProjectSyncer(project).a_sync() async for project in projects]
        await gather(*project_tasks)
        self.stdout.write("Finished syncing all projects")
