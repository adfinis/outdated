from asyncio import gather, run, sleep
from datetime import datetime
from os.path import basename
from re import findall

from aiohttp import ClientSession, client_exceptions
from asgiref.sync import sync_to_async
from dateutil import parser
from django.conf import settings
from yaml import safe_load

from outdated.outdated.models import Dependency, DependencyVersion, Project

NPM_FILES = ["yarn.lock", "pnpm-lock.yaml"]
PYPI_FILES = ["poetry.lock"]

LOCK_FILES = [*NPM_FILES, *PYPI_FILES]

INCLUDED_DEPENDENCIES = [
    "django",
    "django-environ",
    "django-filter",
    "django-hurricane",
    "djangorestframework",
    "djangorestframework-jsonapi",
    "ember-source",
    "ember-data",
    "ember-cli",
    "ember-cli-mirage",
    "ember-validated-form",
    "@embroider/core",
    "mozilla-django-oidc",
]


class ProjectSyncer:
    def __init__(self, project: Project):
        self.project = project
        self.owner, self.name = findall(r"\/([^\/]+)\/([^\/]+)$", self.project.repo)[0]

    async def _get_lockfile_data(self, lockfile):
        async with ClientSession(
            headers={
                "Authorization": f"Bearer {settings.GITHUB_TOKEN}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
            }
        ) as session:
            async with session.get(lockfile["url"]) as response:
                url = (await response.json())["download_url"]
                name = basename(url)
                async with session.get(url) as lockfile_response:
                    return {
                        "name": name,
                        "data": await lockfile_response.text(),
                    }

    async def _get_dependencies(self):
        """Get the dependencies from the lockfiles."""
        q = f"{' '.join(['filename:'+lockfile for lockfile in LOCK_FILES])} repo:{self.owner}/{self.name}"
        async with ClientSession(
            headers={
                "Authorization": f"Bearer {settings.GITHUB_TOKEN}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
            }
        ) as session:
            async with session.get(
                "https://api.github.com/search/code", params={"q": q}
            ) as response:
                json = await response.json()
                if json.get("message") == "Bad credentials":
                    raise ValueError("API Token is not set")  # pragma: no cover
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
                for lockfile in json["items"]:
                    lockfile_tasks.append(session.get(lockfile["url"]))
                for lockfile_task in await gather(*lockfile_tasks):
                    lockfile = await lockfile_task.json()
                    lockfile_data = await self._get_lockfile_data(lockfile)
                    lockfiles.append(lockfile_data)
                return await LockFileParser(lockfiles).parse()

    def sync(self):
        """Sync the project with the remote project."""
        run(self.a_sync())

    async def a_sync(self):
        """Sync the project with the remote project."""
        dependencies = await self._get_dependencies()
        await sync_to_async(self.project.dependency_versions.set)(dependencies)


class LockFileParser:
    """Parse a lockfile and return a list of dependencies."""

    def __init__(self, lockfiles: list[dict]):
        self.lockfiles = lockfiles

    def _get_provider(self, name: str):
        """Get the provider of the lockfile."""
        if name in NPM_FILES:
            return "NPM"
        return "PIP"

    async def _get_version(self, dependency_name_version: tuple, provider: str):
        release_date = None
        dependency = await Dependency.objects.aget_or_create(
            name=dependency_name_version[0], provider=provider
        )

        dependency_version = await DependencyVersion.objects.aget_or_create(
            dependency=dependency[0],
            version=dependency_name_version[1],
        )
        if dependency[1] or dependency_version[1]:
            release_date = await self._get_release_date(dependency_version[0])
            dependency_version[0].release_date = release_date
            await sync_to_async(dependency_version[0].save)()

        return dependency_version[0]

    async def _get_release_date(self, dependency_version: DependencyVersion):
        """Get the release date of a dependency."""
        name = dependency_version.dependency.name
        version = dependency_version.version
        provider = dependency_version.dependency.provider

        try:
            if provider == "NPM":
                async with ClientSession() as session:
                    async with session.get(
                        f"https://registry.npmjs.org/{name}"
                    ) as response:
                        json = await response.json()
                        if json.get("error") == "Not Found":
                            raise ValueError(
                                f"Package {name}@{version} not found"
                            )  # pragma: no cover
                        release_date = json["time"][version]

            elif provider == "PIP":
                async with ClientSession() as session:
                    async with session.get(
                        f"https://pypi.org/pypi/{name}/{version}/json"
                    ) as response:
                        release_date = (await response.json())["urls"][0]["upload_time"]
            return parser.parse(release_date).date()
        except (
            client_exceptions.ClientOSError,
            client_exceptions.ServerDisconnectedError,
        ):  # pragma: no cover
            await sleep(1)
            return await self._get_release_date(dependency_version)

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
            elif name == "pnpm-lock.yaml":
                lockfile = safe_load(data)
                if float(lockfile["lockfileVersion"]) < 6.0:
                    regex = r"\/([^\s]+)\/([^_\s]+).*"
                else:
                    regex = r"\/(@?[^\s@]+)@([^()]+).*"
                dependencies = [
                    findall(regex, dependency)[0]
                    for dependency in lockfile["packages"].keys()
                ]
            matches = dependencies or findall(regex, data)
            tasks.extend(
                [
                    self._get_version(match, provider)
                    for match in matches
                    if match[0] in INCLUDED_DEPENDENCIES
                ]
            )

        return await gather(*tasks)
