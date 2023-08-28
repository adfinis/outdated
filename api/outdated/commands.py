from functools import reduce
from operator import or_

from django.core.management.base import BaseCommand, CommandParser
from django.db.models import Q

from outdated.outdated.models import Project


class ProjectCommand(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        projects = parser.add_mutually_exclusive_group(required=True)
        projects.add_argument(
            "--all",
            action="store_true",
            help="Affect all projects",
        )
        projects.add_argument("projects", nargs="*", type=str, default=[])

    def handle(self, *args, **options):
        if not options["all"]:
            project_names = options["projects"]
            q = reduce(or_, (Q(name__iexact=name) for name in project_names))
            projects = Project.objects.filter(q)
            if projects.count() != len(project_names):
                missing_projects = list(
                    set(project_names).difference(
                        projects.values_list("name", flat=True),
                    ),
                )
                missing_projects.sort()
                self.stderr.write(
                    f"Projects with names {', '.join(missing_projects)} do not exist",
                )
                return
        else:
            projects = Project.objects.all()

        for project in projects:
            self._handle(project)

    def _handle(self, project: Project) -> None:  # pragma: no cover
        raise NotImplementedError
