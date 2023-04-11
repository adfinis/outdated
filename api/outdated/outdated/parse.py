from os.path import basename
from re import findall
from typing import Union

from dateutil import parser
from requests import Session
from yaml import load

from outdated.outdated.models import Dependency, DependencyVersion

NPM_FILES = ["yarn.lock", "pnpm-lock.yaml"]
PYPI_FILES = ["poetry.lock"]


def parse(lockfile: Union[str, list[str]], **kwargs) -> list[dict]:
    if isinstance(lockfile, list):
        return [
            dependency
            for lockfile in lockfile
            for dependency in _ParseLockFile(lockfile)._parse(**kwargs)
        ]
    return _ParseLockFile(lockfile)._parse(**kwargs)


class _ParseLockFile:
    def __init__(self, lockfile: str):
        self.lockfile = lockfile
        self.session = Session()
        self.lockfile = {
            "name": basename(self.lockfile),
            "data": self.session.get(self.lockfile).text,
        }
        self.provider = self._get_provider()

    def _get_lockfile(self):
        """Validate the lockfile."""
        return self.session.get(self.lockfile).text

    def _get_provider(self):
        if self.lockfile["name"] in NPM_FILES:
            return "NPM"
        return "PIP"

    def _get_dependency(self, dependency: tuple):
        return DependencyVersion.objects.get_or_create(
            dependency=Dependency.objects.get_or_create(name=dependency[0])[0],
            version=dependency[1],
            release_date=self._get_release_date(dependency),
        )[0]

    def _get_release_date(self, dependency: tuple):
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

        if release_date:
            return parser.parse(release_date).date()
        return None

    def _parse(
        self,
        whitelisted: list[str] = None,
        blacklisted: list[str] = None,
    ):
        """Parse the lockfile and return a dictionary of dependencies."""
        whitelisted = whitelisted or []
        blacklisted = blacklisted or []
        lockfile_name = self.lockfile["name"]
        if lockfile_name == "yarn.lock":
            regex = r'"?([\S^@]+)@.*:\n  version "(.+)"'
        elif lockfile_name == "poetry.lock":
            regex = r'\[\[package]]\nname = "(.+)"\nversion = "(.+)"'
        elif lockfile_name == "pnpm-lock.yaml":
            return [
                self._get_dependency(dependency)
                for dependency in load(self.lockfile["data"])["specifiers"].items()
                if dependency[0] not in blacklisted
                and (not whitelisted or dependency[0] in whitelisted)
            ]
        else:
            raise ValueError("lockfile not supported yet")
        return [
            self._get_dependency(dependency)
            for dependency in findall(regex, self.lockfile["data"])
            if dependency[0] not in blacklisted
            and (not whitelisted or dependency[0] in whitelisted)
        ]
