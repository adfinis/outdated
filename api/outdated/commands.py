from django.core.management.base import BaseCommand, CommandParser

from outdated.outdated.models import Project


class ProjectCommand(BaseCommand):
    def add_arguments(self, parser: CommandParser):
        projects = parser.add_mutually_exclusive_group(required=True)
        projects.add_argument(
            "--all",
            action="store_true",
            help="Affect all projects",
        )
        projects.add_argument("projects", nargs="*", type=str, default=[])

    def handle(self, *args, **options):
        projects = []
        if not options["all"]:
            nonexistant_projects = []
            project_names = options["projects"]
            for name in project_names:
                try:
                    projects.append(Project.objects.get(name__iexact=name))
                except Project.DoesNotExist:
                    nonexistant_projects.append(name)

            if nonexistant_projects:
                self.stderr.write(
                    f"Projects with names {nonexistant_projects} do not exist"
                )
                return
        projects = (
            Project.objects.filter(id__in=[project.pk for project in projects])
            or Project.objects.all()
        )

        for project in projects:
            self._handle(project)

    def _handle(self, project: Project): # pragma: no cover
        raise NotImplementedError()
