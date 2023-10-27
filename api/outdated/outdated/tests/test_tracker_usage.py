from django.urls import reverse
from rest_framework import status

from outdated.outdated.models import Project


def test_serializer(client, project_factory, tracker_init_mock, tracker_mock):

    setup_mock = tracker_mock("setup")
    delete_mock = tracker_mock("delete")

    data = {
        "data": {
            "type": "projects",
            "id": None,
            "attributes": {
                "name": "foo",
                "repo": "github.com/adfinis/outdated",
            },
            "relationships": {},
        }
    }

    url = reverse("project-list")

    response = client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    project = Project.objects.get(name="foo")
    tracker_init_mock.assert_called_once_with(project)
    setup_mock.assert_called_once()
    assert delete_mock.call_count == 0

    url = reverse("project-detail", args=[project.id])

    patch_data = {
        "data": {
            "type": "projects",
            "id": project.id,
            "attributes": {
                "name": "foo",
                "repo": "Github.com/Adfinis/Outdated",
            },
            "relationships": {},
        }
    }

    resp = client.patch(url, patch_data)

    assert resp.status_code == status.HTTP_200_OK

    assert delete_mock.call_count == 0
    setup_mock.assert_called_once()

    patch_data["data"]["attributes"]["repo"] = "github.com/adfinis/mysagw"
    resp = client.patch(url, patch_data)
    assert resp.status_code == status.HTTP_200_OK
    delete_mock.assert_called_once()
    assert setup_mock.call_count == 2
    project.refresh_from_db()
    tracker_init_mock.assert_called_with(project)

    resp = client.delete(url)
    assert resp.status_code == status.HTTP_204_NO_CONTENT

    assert delete_mock.call_count == 2
