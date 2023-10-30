from __future__ import annotations

import logging
from pathlib import Path
from re import findall

from dateutil import parser
from django.conf import settings
from requests import get, post
from semver import Version as SemVer
from tomllib import loads

from outdated.outdated import models

logger = logging.getLogger(__name__)


def basename(path):
    return Path(path).name


NPM_FILES = ["yarn.lock", "pnpm-lock.yaml"]
PYPI_FILES = ["poetry.lock"]

LOCK_FILES = [*NPM_FILES, *PYPI_FILES]


def get_version(version: str) -> str:
    versions = version.split(".")
    return ".".join([*versions, *["0" for _ in range(3 - len(versions))]])


class Synchroniser:
    def __init__(self, project):
        self.project = project
        self.owner, self.name = findall(r"\/([^\/]+)\/([^\/]+)$", self.project.repo)[0]

    def _get_dependencies(self):
        """Get the dependencies from the lockfiles."""
        q = f"""
        {{
            repository(owner: "{self.owner}", name: "{self.name}") {{
                dependencyGraphManifests {{
                    nodes {{
                        blobPath
                    }}
                }}
            }}
        }}
        """

        resp = post(
            "https://api.github.com/graphql",
            headers={
                "Authorization": f"Bearer {settings.GITHUB_API_TOKEN}",
                "Accept": "application/vnd.github.hawkgirl-preview+json",
            },
            json={"query": q},
            timeout=10,
        )

        json = resp.json()

        if json.get("message") == "Bad credentials":  # pragma: no cover
            msg = "API Token is not set"
            raise ValueError(msg)
        if json.get("errors"):  # pragma: no cover
            raise ValueError(json)

        lockfiles = []
        for lockfile in json["data"]["repository"]["dependencyGraphManifests"]["nodes"]:
            if basename(lockfile["blobPath"]) not in LOCK_FILES:
                continue

            url = f"https://raw.githubusercontent.com/{lockfile['blobPath'].replace('blob/', '')}"
            lockfiles.append({"name": basename(url), "data": get(url, timeout=10).text})

        return LockFileParser(lockfiles).parse()

    def sync(self):
        """Sync the project with the remote project."""
        dependencies = self._get_dependencies()
        self.project.versioned_dependencies.set(dependencies)


class LockFileParser:
    """Parse a lockfile and return a list of dependencies."""

    def __init__(self, lockfiles: list[dict]) -> None:
        self.lockfiles = lockfiles

    def _get_provider(self, name: str) -> str:
        """Get the provider of the lockfile."""
        if name in NPM_FILES:
            return "NPM"
        return "PIP"

    def _get_version(self, requirements: tuple, provider: str) -> models.Version:
        dependency, dependency_created = models.Dependency.objects.get_or_create(
            name=requirements[0],
            provider=provider,
        )
        major, minor, patch = SemVer.parse(get_version(requirements[1])).to_tuple()[0:3]

        release_version, _ = models.ReleaseVersion.objects.get_or_create(
            dependency=dependency,
            major_version=major,
            minor_version=minor,
        )

        version, version_created = models.Version.objects.get_or_create(
            release_version=release_version,
            patch_version=patch,
        )

        if dependency_created or version_created:
            version.release_date = self._get_release_date(version)
            version.save()

        return version

    def _get_release_date(self, version):
        """Get the release date of a dependency."""
        dependency = version.release_version.dependency
        name, provider = dependency.name, dependency.provider

        if provider == "NPM":
            resp = get(f"https://registry.npmjs.org/{name}", timeout=10)
            resp.raise_for_status()
            json = resp.json()
            release_date = json["time"][version.version]

        elif provider == "PIP":
            resp = get(
                f"https://pypi.org/pypi/{name}/{version.version}/json",
                timeout=10,
            )
            resp.raise_for_status()
            json = resp.json()
            release_date = json["urls"][0]["upload_time"]

        return parser.parse(release_date).date()

    def parse(self):
        """Parse the lockfile and return a dictionary of dependencies."""
        versions = []
        for lockfile in self.lockfiles:
            name = lockfile["name"]
            data = lockfile["data"]
            provider = self._get_provider(name)

            dependencies = []
            if name == "yarn.lock":
                regex = r'"?([\S]+)@.*:\n  version "(.+)"'
                dependencies = [
                    dependency
                    for dependency in findall(regex, data)
                    if dependency[0] in settings.TRACKED_DEPENDENCIES
                ]
            elif name == "poetry.lock":
                dependencies = [
                    (dependency["name"], dependency["version"])
                    for dependency in loads(data)["package"]
                    if dependency["name"] in settings.TRACKED_DEPENDENCIES
                ]
            versions.extend(
                [
                    self._get_version(dependency, provider)
                    for dependency in dependencies
                ],
            )
        return versions
