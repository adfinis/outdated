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
def test_release_version(client, release_version_factory, _status):
    include = {"include": "dependency"}
    generated_release_version = release_version_factory(
        undefined=_status == "UNDEFINED",
        outdated=_status == "OUTDATED",
        warning=_status == "WARNING",
        up_to_date=_status == "UP-TO-DATE",
    )
    url = reverse("releaseversion-list")
    resp = client.get(url, include)
    assert resp.status_code == status.HTTP_200_OK
    assert len(resp.json()["data"]) == 1
    resp_detailed = client.get(
        reverse("releaseversion-detail", args=[generated_release_version.id]),
        include,
    )
    assert resp_detailed.status_code == status.HTTP_200_OK

    data = resp.json()["data"][0]
    detailed_data = resp_detailed.json()["data"]
    assert data["id"] == detailed_data["id"] == str(generated_release_version.id)
    response_release_version = data["attributes"]
    detailed_response_release_version = detailed_data["attributes"]
    assert (
        response_release_version["status"]
        == detailed_response_release_version["status"]
        == generated_release_version.status
        == _status
    )

    assert (
        response_release_version["end-of-life"]
        == detailed_response_release_version["end-of-life"]
        == (
            str(generated_release_version.end_of_life)
            if not _status == "UNDEFINED"
            else None
        )
    )
    assert (
        response_release_version["major-version"]
        == detailed_response_release_version["major-version"]
        == generated_release_version.major_version
    )
    assert (
        response_release_version["minor-version"]
        == detailed_response_release_version["minor-version"]
        == generated_release_version.minor_version
    )
    assert (
        data["relationships"]["dependency"]["data"]["id"]
        == detailed_data["relationships"]["dependency"]["data"]["id"]
        == str(generated_release_version.dependency.id)
    )


def test_version(client, version_factory):
    generated_version = version_factory()
    url = reverse("version-list")
    resp = client.get(url)
    assert resp.status_code == status.HTTP_200_OK
    assert len(resp.json()["data"]) == 1
    resp_detailed = client.get(reverse("version-detail", args=[generated_version.id]))
    assert resp_detailed.status_code == status.HTTP_200_OK
    data = resp.json()["data"][0]
    detailed_data = resp_detailed.json()["data"]
    assert data["id"] == detailed_data["id"] == str(generated_version.id)
    response_version = data["attributes"]
    detailed_response_version = detailed_data["attributes"]
    assert (
        response_version["patch-version"]
        == detailed_response_version["patch-version"]
        == generated_version.patch_version
    )
    assert (
        response_version["release-date"]
        == detailed_response_version["release-date"]
        == str(generated_version.release_date)
    )
    assert (
        data["relationships"]["release-version"]["data"]["id"]
        == detailed_data["relationships"]["release-version"]["data"]["id"]
        == str(generated_version.release_version.id)
    )


@pytest.mark.parametrize("defined", [True, False])
def test_project(client, project_factory, version_factory, defined):
    generated_project = project_factory(
        versioned_dependencies=[version_factory()] if defined else []
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
            resp_detailed.json()["data"]["relationships"]["versioned-dependencies"][
                "data"
            ],
            generated_project.versioned_dependencies.all(),
        ):
            assert gen_dep_version["id"] == str(resp_dep_version.id)
    else:
        assert not generated_project.versioned_dependencies.first()
        assert generated_project.status == "UNDEFINED"
