import requests
from outdated.outdated.models import Dependency, DependencyVersion, Project
from django.conf import settings
from dateutil.parser import parse
from os.path import basename
import re

headers = {
    "Authorization": f"Bearer {settings.GITHUB_TOKEN}",
    "Accept": "application/vnd.github.hawkgirl-preview+json",
}

# TODO: Add support for other lock files like pnpm and requirements.txt
NPM_FILES = ["yarn.lock", "pnpm-lock.yaml"]
PYPI_FILES = ["poetry.lock"]

LOCK_FILES = [*NPM_FILES, *PYPI_FILES]

PROVIDER_MAP = {
    **{key: "NPM" for key in NPM_FILES},
    **{key: "PIP" for key in PYPI_FILES},
}

INCLUDE_DEPENDENCIES = [
    "ember-source",
    "ember-data",
    "ember-cli",
    "django",
    "djangorestframework",
    "djangorestframeworkjson-api",
    "gunicorn",
    "python",
]


class ProjectSyncer:
    def __init__(self, project: Project):
        self.project = project
        self.owner, self.name = re.findall(r"\/([^\/]+)\/([^\/]+)$", self.project.repo)[
            0
        ]

    def graphql_query(self, query="") -> str:
        query = f"""
        {{
        repository(owner: "{self.owner}", name: "{self.name}") {{
            dependencyGraphManifests{{
                nodes {{
                    filename
                        {query}
                        }}    
                    }}
                }}
            }}
            """
        return query

    def graphql_request(self, query: str) -> dict:
        response = requests.post(
            "https://api.github.com/graphql",
            json={"query": query},
            headers=headers,
        ).json()

        return response

    def get_all_manifests(self) -> list[str]:
        return [
            manifest["filename"]
            for manifest in self.graphql_request(self.graphql_query())["data"][
                "repository"
            ]["dependencyGraphManifests"]["nodes"]
            if basename(manifest["filename"]) in LOCK_FILES
        ]

    def get_release_date(self, name, version, provider) -> str:
        try:
            if provider == "NPM":
                return requests.get(f"https://registry.npmjs.org/{name}").json()[
                    "time"
                ][version]

            elif provider == "PIP":
                return requests.get(
                    f"https://pypi.org/pypi/{name}/{version}/json"
                ).json()["urls"][1]["upload_time"]
        except Exception as e:
            print(e)

    def get_dependency_version(self, dependency, lock_file) -> dict:
        # remove the '= ' from the beginning of the version
        name = dependency["packageName"]
        version = dependency["requirements"][2:]
        release_date = self.get_release_date(name, version, PROVIDER_MAP[lock_file])

        return {
            "dependency": Dependency.objects.get_or_create(name=name)[0],
            "version": version,
            "release_date": parse(release_date).date(),
        }

    def get_dependencies_from_lock_file(self, filename) -> list[dict]:
        """Get dependencies from a large something.lock file"""
        cur = None
        after = ""
        dependencies = []
        hasNextPage = True
        while hasNextPage:
            query = self.graphql_query(
                f"""
                dependencies{after}{{
                    totalCount
                    pageInfo {{
                        hasNextPage
                        endCursor
                    }}
                    nodes {{
                        packageName
                        requirements
                    }}
                }}
            """
            )
            response = self.graphql_request(query)
            try:
                lock_manifest = [
                    manifest
                    for manifest in response["data"]["repository"][
                        "dependencyGraphManifests"
                    ]["nodes"]
                    if filename in manifest["filename"]
                ]
                if not lock_manifest:
                    break
                lock_manifest = lock_manifest[0]

                hasNextPage = lock_manifest["dependencies"]["pageInfo"]["hasNextPage"]
                dependencies.extend(
                    [
                        dependency
                        for dependency in lock_manifest["dependencies"]["nodes"]
                        if dependency["packageName"] in INCLUDE_DEPENDENCIES
                    ]
                )
                cur = lock_manifest["dependencies"]["pageInfo"]["endCursor"]
                after = f'(after: "{cur}")'
            except Exception as e:
                print(e, response)
        return [
            self.get_dependency_version(dependency, basename(filename))
            for dependency in dependencies
        ]

    def get_project_dependencies(self) -> list[DependencyVersion]:

        dependencies = [
            dependency
            for lock_file in self.get_all_manifests()
            for dependency in self.get_dependencies_from_lock_file(lock_file)
        ]

        return [
            DependencyVersion.objects.get_or_create(**dependency)[0]
            for dependency in dependencies
        ]

    def sync(self):
        self.project.dependency_versions.set(self.get_project_dependencies())
