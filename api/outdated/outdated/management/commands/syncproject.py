from outdated.commands import ProjectCommand
from outdated.outdated.tracking import Tracker


class Command(ProjectCommand):
    help = "Syncs the given project with its remote counterpart."

    def _handle(self, project):
        self.stdout.write(f"Syncing project {project}")
        Tracker(project).sync()
        self.stdout.write(f"Finished syncing {project}")
