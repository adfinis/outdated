import pytest
from django.urls import reverse
from rest_framework import status


def test_dependency(client, dependency_factory):
    generated_dependency = dependency_factory()
    url = reverse("dependency-list")
    resp = client.get(url)
    assert resp.status_code == status.HTTP_200_OK
    assert len(resp.json()["data"]) == 1
    resp_detailed = client.get(
        reverse("dependency-detail", args=[generated_dependency.id])
    )
    assert resp_detailed.status_code == status.HTTP_200_OK
    data = resp.json()["data"][0]
    data_detailed = resp_detailed.json()["data"]
    assert data["id"] == data_detailed["id"] == str(generated_dependency.id)
    response_dependency = data["attributes"]
    detailed_response_dependency = data_detailed["attributes"]
    assert (
        response_dependency["name"]
        == detailed_response_dependency["name"]
        == generated_dependency.name
    )
    assert (
        response_dependency["provider"]
        == detailed_response_dependency["provider"]
        == generated_dependency.provider
    )


@pytest.mark.parametrize("_status", ["UNDEFINED", "OUTDATED", "WARNING", "UP-TO-DATE"])
def test_dependency_version(client, dependency_version_factory, _status):
    include = {"include": "dependency"}
    generated_version = dependency_version_factory(
        undefined=_status == "UNDEFINED",
        outdated=_status == "OUTDATED",
        warning=_status == "WARNING",
        up_to_date=_status == "UP-TO-DATE",
    )
    url = reverse("dependencyversion-list")
    resp = client.get(url, include)
    assert resp.status_code == status.HTTP_200_OK
    assert len(resp.json()["data"]) == 1
    resp_detailed = client.get(
        reverse("dependencyversion-detail", args=[generated_version.id]), include
    )
    assert resp_detailed.status_code == status.HTTP_200_OK
    data = resp.json()["data"][0]
    detailed_data = resp_detailed.json()["data"]
    assert data["id"] == detailed_data["id"] == str(generated_version.id)
    response_version = data["attributes"]
    detailed_response_version = detailed_data["attributes"]
    assert (
        response_version["status"]
        == detailed_response_version["status"]
        == generated_version.status
        == _status
    )

    assert (
        response_version["version"]
        == detailed_response_version["version"]
        == generated_version.version
    )
    assert (
        response_version["release-date"]
        == detailed_response_version["release-date"]
        == str(generated_version.release_date)
    )
    assert (
        response_version["end-of-life-date"]
        == detailed_response_version["end-of-life-date"]
        == (
            str(generated_version.end_of_life_date)
            if not _status == "UNDEFINED"
            else None
        )
    )
    assert (
        data["relationships"]["dependency"]["data"]["id"]
        == detailed_data["relationships"]["dependency"]["data"]["id"]
        == str(generated_version.dependency.id)
    )


@pytest.mark.parametrize("defined", [True, False])
def test_project(client, project_factory, dependency_version_factory, defined):
    generated_project = project_factory(
        dependency_versions=[dependency_version_factory()] if defined else []
    )
    url = reverse("project-list")
    resp = client.get(url)
    assert resp.status_code == status.HTTP_200_OK
    assert len(resp.json()["data"]) == 1
    resp_detailed = client.get(reverse("project-detail", args=[generated_project.id]))
    assert resp_detailed.status_code == status.HTTP_200_OK
    data = resp.json()["data"][0]
    detailed_data = resp_detailed.json()["data"]
    assert data["id"] == detailed_data["id"] == str(generated_project.id)
    response_project = data["attributes"]
    detailed_response_project = detailed_data["attributes"]
    assert (
        response_project["name"]
        == detailed_response_project["name"]
        == generated_project.name
    )
    assert (
        response_project["repo"]
        == detailed_response_project["repo"]
        == generated_project.repo
    )
    if defined:
        for gen_dep_version, resp_dep_version in zip(
            resp_detailed.json()["data"]["relationships"]["dependency-versions"][
                "data"
            ],
            generated_project.dependency_versions.all(),
        ):
            assert gen_dep_version["id"] == str(resp_dep_version.id)
    else:
        assert not generated_project.dependency_versions.first()
        assert generated_project.status == "UNDEFINED"


@pytest.mark.vcr()
@pytest.mark.django_db(transaction=True)
def test_sync_project_endpoint(client, project_factory):
    generated_project = project_factory(repo="https://github.com/adfinis/outdated")
    url = reverse("project-sync", args=[generated_project.id])
    resp = client.post(url)
    assert resp.status_code == status.HTTP_200_OK
    assert generated_project.dependency_versions.count() > 0
