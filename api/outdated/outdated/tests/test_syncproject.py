import pytest
from django.core.management import call_command


@pytest.mark.django_db(transaction=True)
def test_syncproject(project, tracker_mock, tracker_init_mock):
    tracker_sync_mock = tracker_mock("sync")
    call_command("syncproject", project.name)
    tracker_init_mock.assert_called_once_with(project)
    tracker_sync_mock.assert_called_once()
