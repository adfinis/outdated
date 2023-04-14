from datetime import datetime
from os.path import basename
from re import findall
from time import sleep

from dateutil import parser
from django.conf import settings
from requests import Session
from yaml import safe_load

from outdated.outdated.models import Dependency, DependencyVersion, Project

headers = {
    "Authorization": f"Bearer {settings.GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}
NPM_FILES = ["yarn.lock", "pnpm-lock.yaml"]
PYPI_FILES = ["poetry.lock"]

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
        """Get the dependencies from the lockfiles."""
        q = f"{' '.join(['filename:'+lockfile for lockfile in LOCK_FILES])} repo:{self.owner}/{self.name}"
        response = self.session.get(
            "https://api.github.com/search/code", params={"q": q}
        )
        json = response.json()
        headers = response.headers
        if headers.get("X-RateLimit-Remaining") == "0":
            t = int(headers.get("X-RateLimit-Reset")) - int(
                datetime.utcnow().timestamp()
            )
            print(f"Rate limit exceeded. Sleeping for {t} seconds.")
            sleep(t)
            return self.get_dependencies()
        print(response.headers, response.status_code, json)

        lockfiles = [
            self.session.get(lockfile["url"]).json()["download_url"]
            for lockfile in json["items"]
        ]

        return self.parse_lockfiles(lockfiles)

    def sync(self):
        """Sync the project with the remote project."""
        dependencies = self.get_dependencies()
        if dependencies:
            self.project.dependency_versions.set(dependencies)

    def parse_lockfiles(self, lockfiles: list[str]) -> list[dict]:
        """Parse one or more lockfiles and return a list of dependencies."""
        return [
            dependency
            for lockfile in lockfiles
            for dependency in LockFileParser(lockfile)._parse()
        ]


class LockFileParser:
    """Parse a lockfile and return a list of dependencies."""

    def __init__(self, lockfile: str):
        self.lockfile = lockfile
        self.session = Session()
        self.lockfile = {
            "name": basename(self.lockfile),
            "data": self.session.get(self.lockfile).text,
        }
        self.provider = self._get_provider()

    def _get_provider(self):
        """Get the provider of the lockfile."""
        if self.lockfile["name"] in NPM_FILES:
            return "NPM"
        return "PIP"

    def _get_version(self, dependency: tuple):
        try:
            version = DependencyVersion.objects.get(
                dependency__name=dependency[0],
                dependency__provider=self.provider,
                version=dependency[1],
            )
        except DependencyVersion.DoesNotExist:
            version = DependencyVersion.objects.create(
                dependency=Dependency.objects.get_or_create(
                    name=dependency[0], provider=self.provider
                )[0],
                version=dependency[1],
                release_date=self._get_release_date(dependency),
            )
        return version

    def _get_release_date(self, dependency: tuple):
        """Get the release date of a dependency."""
        name = dependency[0]
        version = dependency[1]
        if self.provider == "NPM":
            release_date = self.session.get(
                f"https://registry.npmjs.org/{name}"
            ).json()["time"][version]

        elif self.provider == "PIP":
            release_date = self.session.get(
                f"https://pypi.org/pypi/{name}/{version}/json"
            ).json()["urls"][1]["upload_time"]

        return parser.parse(release_date).date()

    def _parse(self):
        """Parse the lockfile and return a dictionary of dependencies."""
        lockfile_name = self.lockfile["name"]
        data = self.lockfile["data"]
        dependencies = []
        if lockfile_name == "yarn.lock":
            regex = r'"?([\S@]+)@.*:\n  version "(.+)"'
        elif lockfile_name == "poetry.lock":
            regex = r'\[\[package]]\nname = "(.+)"\nversion = "(.+)"'
        elif lockfile_name == "pnpm-lock.yaml":
            lockfile = safe_load(data)
            if float(lockfile["lockfileVersion"]) < 6.0:
                regex = r"\/([^\s_]+)\/([^_\s]+).*"
            else:
                regex = r"\/(@?[^\s@]+)@([^()]+).*"
            print(lockfile["packages"].keys())
            dependencies = [
                findall(regex, dependency)[0]
                for dependency in lockfile["packages"].keys()
            ]
            print(dependencies)
        else:
            raise ValueError("Lockfile not supported yet")  # pragma: no cover
        return [
            self._get_version(dependency)
            for dependency in dependencies or findall(regex, data)
        ]
