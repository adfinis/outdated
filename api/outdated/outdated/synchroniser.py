from asyncio import gather, run, sleep
from datetime import datetime
from os.path import basename
from re import findall

from aiohttp import ClientSession, client_exceptions
from asgiref.sync import sync_to_async
from dateutil import parser
from django.conf import settings
from semver import Version as SemVer

from outdated.outdated.models import Dependency, Project, ReleaseVersion, Version

# from yaml import safe_load


NPM_FILES = ["yarn.lock", "pnpm-lock.yaml"]
PYPI_FILES = ["poetry.lock"]

LOCK_FILES = [*NPM_FILES, *PYPI_FILES]


def get_version(version: str) -> str:
    versions = version.split(".")
    return ".".join([*versions, *["0" for _ in range(3 - len(versions))]])


class Synchroniser:
    def __init__(self, project: Project):
        self.project = project
        self.owner, self.name = findall(r"\/([^\/]+)\/([^\/]+)$", self.project.repo)[0]

    async def _get_dependencies(self):
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

        async with ClientSession() as session:
            async with session.post(
                "https://api.github.com/graphql",
                headers={
                    "Authorization": f"Bearer {settings.GITHUB_API_TOKEN}",
                    "Accept": "application/vnd.github.hawkgirl-preview+json",
                },
                json={"query": q},
            ) as response:
                json = await response.json()
                if json.get("message") == "Bad credentials":
                    raise ValueError("API Token is not set")  # pragma: no cover
                elif json.get("errors") and json["errors"][0]["message"] == "timedout":
                    return await self._get_dependencies()  # pragma: no cover
                elif json.get("errors"):
                    raise ValueError(json)  # pragma: no cover
                headers = response.headers
                if headers.get("X-RateLimit-Remaining") == "0":  # pragma: no cover
                    t = (
                        int(headers.get("X-RateLimit-Reset"))
                        - int(datetime.utcnow().timestamp())
                    ) / 1000
                    print(f"Rate limit exceeded. Sleeping for {t} seconds.")
                    await sleep(t)
                    return await self._get_dependencies()

                lockfiles = []
                lockfile_tasks = []
                for lockfile in json["data"]["repository"]["dependencyGraphManifests"][
                    "nodes"
                ]:
                    if basename(lockfile["blobPath"]) in LOCK_FILES:
                        url = f"https://raw.githubusercontent.com/{lockfile['blobPath'].replace(f'blob/', f'')}"
                        lockfile_tasks.append(session.get(url))
                for lockfile_task in await gather(*lockfile_tasks):
                    lockfiles.append(
                        {
                            "name": basename(str(lockfile_task.url)),
                            "data": await lockfile_task.text(),
                        }
                    )

                return await LockFileParser(lockfiles).parse()

    def sync(self):
        """Sync the project with the remote project."""
        run(self.a_sync())

    async def a_sync(self):
        """Sync the project with the remote project."""
        dependencies = await self._get_dependencies()
        await sync_to_async(self.project.versioned_dependencies.set)(dependencies)


class LockFileParser:
    """Parse a lockfile and return a list of dependencies."""

    def __init__(self, lockfiles: list[dict]):
        self.lockfiles = lockfiles

    def _get_provider(self, name: str):
        """Get the provider of the lockfile."""
        if name in NPM_FILES:
            return "NPM"
        return "PIP"

    async def _get_version(self, requirements: tuple, provider: str):
        dependency, dependency_created = await Dependency.objects.aget_or_create(
            name=requirements[0], provider=provider
        )
        major, minor, patch = SemVer.parse(get_version(requirements[1])).to_tuple()[0:3]

        release_version, _ = await ReleaseVersion.objects.aget_or_create(
            dependency=dependency,
            major_version=major,
            minor_version=minor,
        )

        version, version_created = await Version.objects.aget_or_create(
            release_version=release_version,
            patch_version=patch,
        )

        if dependency_created or version_created:
            version.release_date = await self._get_release_date(version)
            await sync_to_async(version.save)()

        return version

    async def _get_release_date(self, version: Version):
        """Get the release date of a dependency."""
        dependency = version.release_version.dependency
        name, provider = dependency.name, dependency.provider

        try:
            if provider == "NPM":
                async with ClientSession() as session:
                    async with session.get(
                        f"https://registry.npmjs.org/{name}"
                    ) as response:
                        response.raise_for_status()
                        json = await response.json()
                        release_date = json["time"][version.version]

            elif provider == "PIP":
                async with ClientSession() as session:
                    async with session.get(
                        f"https://pypi.org/pypi/{name}/{version.version}/json"
                    ) as response:
                        response.raise_for_status()
                        release_date = (await response.json())["urls"][0]["upload_time"]
            return parser.parse(release_date).date()
        except (
            client_exceptions.ClientOSError,
            client_exceptions.ServerDisconnectedError,
        ):  # pragma: no cover
            await sleep(1)
            return await self._get_release_date(version)

    async def parse(self):
        """Parse the lockfile and return a dictionary of dependencies."""
        tasks = []
        for lockfile in self.lockfiles:
            name = lockfile["name"]
            data = lockfile["data"]
            provider = self._get_provider(name)

            dependencies = []
            if name == "yarn.lock":
                regex = r'"?([\S]+)@.*:\n  version "(.+)"'
            elif name == "poetry.lock":
                regex = r'\[\[package]]\nname = "(.+)"\nversion = "(.+)"'
            #            elif name == "pnpm-lock.yaml":  # pragma: no cover
            #               lockfile = safe_load(data)
            #              if float(lockfile["lockfileDependencyVersion"]) < 6.0:
            #                  regex = r"\/([^\s]+)\/([^_\s]+).*"
            #              else:
            #                    regex = r"\/(@?[^\s@]+)@([^()]+).*"
            #                dependencies = [
            #                    findall(regex, dependency)[0]
            #                    for dependency in lockfile["packages"].keys()
            #                ]
            matches = dependencies or findall(regex, data)
            tasks.extend(
                [
                    self._get_version(match, provider)
                    for match in matches
                    if match[0] in settings.RELEVANT_DEPENDENCIES
                ]
            )

        return await gather(*tasks)
