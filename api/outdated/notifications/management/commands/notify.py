from outdated.commands import ProjectCommand
from outdated.notifications.notifier import Notifier


class Command(ProjectCommand):
    help = "Send notifications to given projects."

    def _handle(self, project):
        if not project.maintainers.all():
            self.stdout.write(
                f"Skipped {project.name} (no-maintainers)", self.style.WARNING
            )
            return
        elif project.duration_until_outdated is None:
            return

        Notifier(project).notify()
        self.stdout.write(f"Notified {project}", self.style.SUCCESS)
