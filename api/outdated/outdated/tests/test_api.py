import pytest
from django.urls import reverse
from rest_framework import status as http_status

from outdated.outdated.models import Maintainer


def test_dependency(client, dependency_factory):
    generated_dependency = dependency_factory()
    url = reverse("dependency-list")
    resp = client.get(url)
    assert resp.status_code == http_status.HTTP_200_OK
    assert len(resp.json()["data"]) == 1
    resp_detailed = client.get(
        reverse("dependency-detail", args=[generated_dependency.id]),
    )
    assert resp_detailed.status_code == http_status.HTTP_200_OK
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


@pytest.mark.parametrize("status", ["UNDEFINED", "OUTDATED", "WARNING", "UP-TO-DATE"])
def test_release_version(client, release_version_factory, status):
    include = {"include": "dependency"}
    generated_release_version = release_version_factory(
        undefined=status == "UNDEFINED",
        outdated=status == "OUTDATED",
        warning=status == "WARNING",
        up_to_date=status == "UP-TO-DATE",
    )
    url = reverse("releaseversion-list")
    resp = client.get(url, include)
    assert resp.status_code == http_status.HTTP_200_OK
    assert len(resp.json()["data"]) == 1
    resp_detailed = client.get(
        reverse("releaseversion-detail", args=[generated_release_version.id]),
        include,
    )
    assert resp_detailed.status_code == http_status.HTTP_200_OK

    data = resp.json()["data"][0]
    detailed_data = resp_detailed.json()["data"]
    assert data["id"] == detailed_data["id"] == str(generated_release_version.id)
    response_release_version = data["attributes"]
    detailed_response_release_version = detailed_data["attributes"]
    assert (
        response_release_version["status"]
        == detailed_response_release_version["status"]
        == generated_release_version.status
        == status
    )

    assert (
        response_release_version["end-of-life"]
        == detailed_response_release_version["end-of-life"]
        == (
            str(generated_release_version.end_of_life)
            if status != "UNDEFINED"
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
    assert resp.status_code == http_status.HTTP_200_OK
    assert len(resp.json()["data"]) == 1
    resp_detailed = client.get(reverse("version-detail", args=[generated_version.id]))
    assert resp_detailed.status_code == http_status.HTTP_200_OK
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
def test_project(
    client, project_factory, dependency_source_factory, version_factory, defined
):
    generated_project = project_factory()
    dependency_source_factory(
        versions=[version_factory()] if defined else [], project=generated_project
    )

    url = reverse("project-list")
    resp = client.get(url)
    assert resp.status_code == http_status.HTTP_200_OK
    assert len(resp.json()["data"]) == 1
    resp_detailed = client.get(reverse("project-detail", args=[generated_project.id]))
    assert resp_detailed.status_code == http_status.HTTP_200_OK
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
    assert (
        response_project["repo-type"]
        == detailed_response_project["repo-type"]
        == generated_project.repo_type
    )
    if defined:
        for gen_dep_version, resp_dep_version in zip(
            resp_detailed.json()["data"]["relationships"]["sources"]["data"],
            generated_project.sources.all(),
        ):
            assert gen_dep_version["id"] == str(resp_dep_version.id)
    else:
        assert not generated_project.sources.first().versions.first()
        assert generated_project.sources.first().status == "UNDEFINED"
        assert generated_project.status == "UNDEFINED"


def test_project_ordered_by_eol(
    client,
    project_factory,
    dependency_source_factory,
    release_version_factory,
    version_factory,
):
    outdated_version = version_factory(
        release_version=release_version_factory(outdated=True),
    )
    warning_version = version_factory(
        release_version=release_version_factory(warning=True),
    )
    up_to_date_version = version_factory(
        release_version=release_version_factory(up_to_date=True),
    )

    project_up_to_date = project_factory(name="A project")
    dependency_source_factory(versions=[up_to_date_version], project=project_up_to_date)
    project_warning = project_factory(name="B project")
    dependency_source_factory(versions=[warning_version], project=project_warning)
    project_outdated = project_factory(name="C project")
    dependency_source_factory(versions=[outdated_version], project=project_outdated)
    project_undefined = project_factory(name="D project")

    url = reverse("project-list")
    resp = client.get(url)
    assert resp.status_code == http_status.HTTP_200_OK
    json = resp.json()

    assert json["data"][0]["id"] == str(project_outdated.pk)
    assert json["data"][1]["id"] == str(project_warning.pk)
    assert json["data"][2]["id"] == str(project_up_to_date.pk)
    assert json["data"][3]["id"] == str(project_undefined.pk)


def test_maintainer(client, maintainer):
    assert Maintainer.objects.count() == 1
    url = reverse("maintainer-list")
    resp = client.get(url)
    assert resp.status_code == http_status.HTTP_200_OK
    resp_detailed = client.get(reverse("maintainer-detail", args=[maintainer.id]))
    relationships = resp.json()["data"][0]["relationships"]
    detailed_relationships = resp_detailed.json()["data"]["relationships"]

    assert (
        relationships["user"]["data"]["id"]
        == detailed_relationships["user"]["data"]["id"]
        == str(maintainer.user.id)
    )
    assert (
        relationships["source"]["data"]["id"]
        == detailed_relationships["source"]["data"]["id"]
        == str(maintainer.source.id)
    )
    assert (
        resp.json()["data"][0]["attributes"]
        == resp_detailed.json()["data"]["attributes"]
    )
    assert maintainer.source.maintainers.all()[0] == maintainer


@pytest.mark.django_db(transaction=True)
def test_sync_project_endpoint(client, project, tracker_init_mock, tracker_mock):
    tracker_sync_mock = tracker_mock("sync")
    url = reverse("project-sync", args=[project.id])
    resp = client.post(url)
    assert resp.status_code == http_status.HTTP_200_OK
    tracker_init_mock.assert_called_once_with(project)
    tracker_sync_mock.assert_called_once()
