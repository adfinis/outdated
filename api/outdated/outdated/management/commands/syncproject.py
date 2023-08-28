from outdated.commands import ProjectCommand
from outdated.outdated.synchroniser import Synchroniser


class Command(ProjectCommand):
    help = "Syncs the given project with its remote counterpart."

    def _handle(self, project):
        self.stdout.write(f"Syncing project {project}")
        Synchroniser(project).sync()
        self.stdout.write(f"Finished syncing {project}")
