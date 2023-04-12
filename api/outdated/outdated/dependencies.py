from re import findall

from django.conf import settings
from requests import Session

from outdated.outdated.models import Project
from outdated.outdated.parse import NPM_FILES, PYPI_FILES, parse

headers = {
    "Authorization": f"Bearer {settings.GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}

LOCK_FILES = [*NPM_FILES, *PYPI_FILES]

INCLUDE_DEPENDENCIES = [
    "@embroider/core",
    "ember-source",
    "ember-data",
    "ember-cli",
    "django",
    "djangorestframework",
    "djangorestframeworkjson-api",
    "django-filter",
    "django-hurricane",
    "gunicorn",
    "python",
]


class ProjectSyncer:
    def __init__(self, project: Project):
        self.project = project
        self.owner, self.name = findall(r"\/([^\/]+)\/([^\/]+)$", self.project.repo)[0]
        self.session = Session()
        self.session.headers.update(headers)

    def get_dependencies(self):
        q = f"{' '.join(['filename:'+lockfile for lockfile in LOCK_FILES])} repo:{self.owner}/{self.name}"
        lockfiles = [
            self.session.get(lockfile["url"]).json()["download_url"]
            for lockfile in self.session.get(
                "https://api.github.com/search/code", params={"q": q}
            ).json()["items"]
        ]
        return parse(lockfiles, whitelisted=INCLUDE_DEPENDENCIES)

    def sync(self):
        dependencies = self.get_dependencies()
        if dependencies:
            self.project.dependency_versions.set(dependencies)
