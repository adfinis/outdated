from datetime import datetime

from rest_framework import status


def test_dependency(
    client,
    dependency_factory,
):

    gen_dependencies = dependency_factory.create_batch(2)
    resp = client.get("/dependencies/")
    assert resp.status_code == status.HTTP_200_OK
    assert len(resp.json()["data"]) == 2
    for gen_dependency in gen_dependencies:
        resp_detailed = client.get(f"/dependencies/{gen_dependency.id}/")

        assert resp_detailed.status_code == status.HTTP_200_OK
        assert resp_detailed.json()["data"]["attributes"]["name"] == gen_dependency.name


def test_dependency_versions(
    client, date_format, dependency_factory, dependency_version_factory
):
    included = {"include": "dependency"}
    dependency_factory.create_batch(2)
    n = 5
    gen_dep_versions = dependency_version_factory.create_batch(n)

    resp = client.get("/dependency-versions/", included)
    assert resp.status_code == status.HTTP_200_OK
    assert len(resp.json()["data"]) == n
    for gen_dep_version in gen_dep_versions:

        resp_detailed = client.get(
            f"/dependency-versions/{gen_dep_version.id}/", included
        )

        assert resp_detailed.status_code == status.HTTP_200_OK

        resp_dep_version = resp_detailed.json()["data"]["attributes"]
        assert (
            int(
                resp_detailed.json()["data"]["relationships"]["dependency"]["data"][
                    "id"
                ]
            )
            == gen_dep_version.dependency.id
        )
        assert resp_dep_version["status"] == gen_dep_version.status
        assert resp_dep_version["version"] == gen_dep_version.version
        assert (
            datetime.strptime(resp_dep_version["release-date"], date_format).date()
            == gen_dep_version.release_date
        )
        assert (
            datetime.strptime(resp_dep_version["eol-date"], date_format).date()
            == gen_dep_version.eol_date
        )


def test_project(
    client,
    dependency_factory,
    dependency_version_factory,
    project_factory,
):
    n = 4
    included = {"include": "dependency-versions,dependency-versions.dependency"}
    dependency_factory.create_batch(10)
    gen_projects = [
        project_factory.create(
            dependency_versions=dependency_version_factory.create_batch(3)
        )
        for _ in range(n)
    ]
    resp = client.get("/projects/", included)
    assert len(resp.json()["data"]) == n
    assert resp.status_code == status.HTTP_200_OK
    for gen_project in gen_projects:
        resp_detailed = client.get(f"/projects/{gen_project.id}/", included)
        assert resp_detailed.status_code == status.HTTP_200_OK
