from datetime import date, timedelta
from uuid import UUID

import pytest
from django.urls import reverse
from rest_framework import status


def test_dependency(
    client,
    dependency_factory,
):

    gen_dependency = dependency_factory.create()
    url = reverse("dependency-list")
    resp = client.get(url)
    assert resp.status_code == status.HTTP_200_OK
    assert len(resp.json()["data"]) == 1
    url = reverse("dependency-detail", args=[gen_dependency.id])
    resp_detailed = client.get(url)

    assert resp_detailed.status_code == status.HTTP_200_OK
    assert resp_detailed.json()["data"]["attributes"]["name"] == gen_dependency.name


@pytest.mark.parametrize("_status", ["OUTDATED", "WARNING", "UP_TO_DATE"])
def test_dependency_versions(
    client, str_to_date, dependency_factory, dependency_version_factory, _status
):
    include = {"include": "dependency"}
    dependency_factory.create_batch(2)
    gen_dep_version = dependency_version_factory.create(
        outdated=_status == "OUTDATED",
        warning=_status == "WARNING",
        up_to_date=_status == "UP_TO_DATE",
    )
    url = reverse("dependencyversion-list")
    print(url)
    resp = client.get(url, include)
    assert resp.status_code == status.HTTP_200_OK
    assert len(resp.json()["data"]) == 1

    resp_detailed = client.get(
        reverse("dependencyversion-detail", args=[gen_dep_version.id]), include
    )

    assert resp_detailed.status_code == status.HTTP_200_OK

    resp_dep_version = resp_detailed.json()["data"]["attributes"]
    assert (
        UUID(resp_detailed.json()["data"]["relationships"]["dependency"]["data"]["id"])
        == gen_dep_version.dependency.id
    )

    _status = resp_dep_version["status"]
    eol_date = str_to_date(resp_dep_version["eol-date"])

    today = date.today()
    assert _status == gen_dep_version.status
    if today >= eol_date:
        assert _status == "OUTDATED"
    elif today + timedelta(days=30) >= eol_date:
        assert _status == "WARNING"
    else:
        assert _status == "UP-TO-DATE"

    assert resp_dep_version["version"] == gen_dep_version.version
    assert eol_date == gen_dep_version.eol_date
    assert str_to_date(resp_dep_version["release-date"]) == gen_dep_version.release_date


@pytest.mark.parametrize("defined", [False, True])
def test_project(
    client,
    defined,
    dependency_factory,
    dependency_version_factory,
    project_factory,
):
    included = {"include": "dependency-versions,dependency-versions.dependency"}
    dependency_factory.create_batch(5)

    gen_project = project_factory.create(
        dependency_versions=dependency_version_factory.create_batch(5)
        if defined
        else None
    )

    url = reverse("project-list")
    resp = client.get(url, included)
    assert len(resp.json()["data"]) == 1
    assert resp.status_code == status.HTTP_200_OK
    url = reverse("project-detail", args=[gen_project.id])
    resp_detailed = client.get(url, included)
    assert resp_detailed.status_code == status.HTTP_200_OK
    resp_project = resp_detailed.json()["data"]["attributes"]
    assert resp_project["status"] == gen_project.status
    assert resp_project["name"] == gen_project.name
    assert resp_project["repo"] == gen_project.repo
    if defined:
        for gen_dep_version, resp_dep_version in zip(
            resp_detailed.json()["data"]["relationships"]["dependency-versions"][
                "data"
            ],
            gen_project.dependency_versions.all(),
        ):
            assert UUID(gen_dep_version["id"]) == resp_dep_version.id
    else:
        assert not gen_project.dependency_versions.first()
        assert gen_project.status == "UNDEFINED"
