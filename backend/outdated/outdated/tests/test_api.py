from datetime import date, timedelta

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
    client, str_to_date, dependency_factory, dependency_version_factory
):
    included = {"include": "dependency"}
    dependency_factory.create_batch(2)
    gen_dep_versions = [
        dependency_version_factory.create(outdated=True),
        dependency_version_factory.create(warning=True),
        dependency_version_factory.create(up_to_date=True),
    ]

    resp = client.get("/dependency-versions/", included)
    assert resp.status_code == status.HTTP_200_OK
    assert len(resp.json()["data"]) == 3
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

        _status = resp_dep_version["status"]
        eol_date = str_to_date(resp_dep_version["eol-date"])

        today = date.today()
        if today >= eol_date:
            assert _status == "OUTDATED"
        elif today + timedelta(days=30) >= eol_date:
            assert _status == "WARNING"
        else:
            assert _status == "UP-TO-DATE"
        assert _status == gen_dep_version.status
        assert resp_dep_version["version"] == gen_dep_version.version
        assert eol_date == gen_dep_version.eol_date
        assert (
            str_to_date(resp_dep_version["release-date"])
            == gen_dep_version.release_date
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
        for _ in range(n - 1)
    ]
    gen_projects.append(project_factory.create())
    resp = client.get("/projects/", included)
    assert len(resp.json()["data"]) == n
    assert resp.status_code == status.HTTP_200_OK
    for gen_project in gen_projects:
        resp_detailed = client.get(f"/projects/{gen_project.id}/", included)
        assert resp_detailed.status_code == status.HTTP_200_OK
        resp_project = resp_detailed.json()["data"]["attributes"]
        assert resp_project["status"] == gen_project.status
        assert resp_project["name"] == gen_project.name
        assert resp_project["repo"] == gen_project.repo
        if gen_project.status != "UNDEFINED":
            for gen_dep_version, resp_dep_version in zip(
                resp_detailed.json()["data"]["relationships"]["dependency-versions"][
                    "data"
                ],
                gen_project.dependency_versions.all(),
            ):
                assert int(gen_dep_version["id"]) == resp_dep_version.id
        else:
            assert not gen_project.dependency_versions.first()
