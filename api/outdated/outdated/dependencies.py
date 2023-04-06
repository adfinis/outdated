from os.path import basename
from re import findall

from dateutil.parser import parse
from django.conf import settings
from requests import get, post

from outdated.outdated.models import Dependency, DependencyVersion

headers = {
    "Authorization": f"Bearer {settings.GITHUB_TOKEN}",
    "Accept": "application/vnd.github.hawkgirl-preview+json",
}

# TODO: Add support for other lock files and a way to support requirements.txt
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
    "ember-cli-htmlbars",
    "django",
    "djangorestframework",
    "djangorestframeworkjson-api",
    "gunicorn",
    "python",
]


class ProjectSyncer:
    def __init__(self, project):
        self.project = project
        self.owner, self.name = findall(r"\/([^\/]+)\/([^\/]+)$", self.project.repo)[0]

    def graphql_query(self, query="") -> str:
        return f"""
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

    def graphql_request(self, query: str) -> dict:
        return post(
            "https://api.github.com/graphql",
            json={"query": query},
            headers=headers,
        ).json()

    def get_dependency_version(self, dependency) -> dict:
        # remove the '= ' from the beginning of the version
        name = dependency["packageName"]
        version = dependency["requirements"][2:]
        provider = dependency["packageManager"]

        if provider == "NPM":
            release_date = get(f"https://registry.npmjs.org/{name}").json()["time"][
                version
            ]

        elif provider == "PIP":
            release_date = get(f"https://pypi.org/pypi/{name}/{version}/json").json()[
                "urls"
            ][1]["upload_time"]
        else:
            raise Exception("Provider not supported yet")

        return {
            "dependency": Dependency.objects.get_or_create(name=name)[0],
            "version": version,
            "release_date": parse(release_date).date(),
        }

    def get_dependencies(self):
        hasNextPage, after, dependencies = True, "", []
        while hasNextPage:
            hasNextPage = False
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
                        packageManager
                    }}
                }}
            """
            )
            manifests = [
                manifest
                for manifest in self.graphql_request(query)["data"]["repository"][
                    "dependencyGraphManifests"
                ]["nodes"]
                if basename(manifest["filename"]) in LOCK_FILES
            ]

            for manifest in manifests:
                if manifest["dependencies"]["pageInfo"]["hasNextPage"]:
                    hasNextPage = True
                    after = f'(after: "{manifest["dependencies"]["pageInfo"]["endCursor"]}")'
                dependencies.extend(
                    [
                        self.get_dependency_version(dependency)
                        for dependency in manifest["dependencies"]["nodes"]
                        if dependency["packageName"] in INCLUDE_DEPENDENCIES
                    ]
                )
        return dependencies

    def get_project_dependencies(self) -> list[DependencyVersion]:

        return [
            DependencyVersion.objects.get_or_create(**dependency)[0]
            for dependency in self.get_dependencies()
        ]

    def sync(self):
        self.project.dependency_versions.set(self.get_project_dependencies())
