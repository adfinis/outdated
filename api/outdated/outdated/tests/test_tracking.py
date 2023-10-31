import pytest
from django.urls import reverse
from rest_framework import status

from outdated.outdated.models import Project


@pytest.mark.parametrize(
    "repo,reinitialize",
    [
        ("github.com/Adfinis/Outdated", False),
        ("github.com/adfinis/outdated", False),
        ("Github.Com/ADFINIS/OutdAted", False),
        ("github.com/adfinis/mysagw", True),
        ("github.com/adfinis/timed-frontend", True),
    ],
)
def test_serializer_patch(
    client,
    project_factory,
    tracker_init_mock,
    tracker_mock,
    repo,
    reinitialize,
):
    project = project_factory(repo="github.com/adfinis/outdated")
    setup_mock = tracker_mock("setup")
    delete_mock = tracker_mock("delete")

    data = {
        "data": {
            "type": "projects",
            "id": project.id,
            "attributes": {
                "name": project.name,
                "repo": repo,
            },
            "relationships": {},
        },
    }

    url = reverse("project-detail", args=[project.id])

    resp = client.patch(url, data)
    assert resp.status_code == status.HTTP_200_OK

    if reinitialize:
        delete_mock.assert_called_once()
        setup_mock.assert_called_once()
        assert tracker_init_mock.call_count == 2
        assert (
            tracker_init_mock.call_args_list[0].args[0].repo
            == "github.com/adfinis/outdated"
        )
        tracker_init_mock.assert_called_with(project)
    else:
        delete_mock.assert_not_called()
        setup_mock.assert_not_called()
        tracker_init_mock.assert_not_called()


def test_serializer_create(client, project_factory, tracker_init_mock, tracker_mock):
    setup_mock = tracker_mock("setup")

    data = {
        "data": {
            "type": "projects",
            "id": None,
            "attributes": {
                "name": "foo",
                "repo": "github.com/adfinis/outdated",
            },
            "relationships": {},
        },
    }

    url = reverse("project-list")

    response = client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    project = Project.objects.get(name="foo")
    tracker_init_mock.assert_called_once_with(project)
    setup_mock.assert_called_once()


def test_view_delete(client, project, tracker_init_mock, tracker_mock):
    delete_mock = tracker_mock("delete")
    url = reverse("project-detail", args=[project.id])
    resp = client.delete(url)
    assert resp.status_code == status.HTTP_204_NO_CONTENT
    tracker_init_mock.assert_called_once()
    delete_mock.assert_called_once()
    assert not Project.objects.filter(id=project.id)
