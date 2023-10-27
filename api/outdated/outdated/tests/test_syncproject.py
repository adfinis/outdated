from unittest.mock import call

import pytest
from django.core.management import call_command

from outdated.tracking import Tracker


@pytest.mark.django_db(transaction=True)
def test_syncproject(project_factory, mocker):

    project = project_factory()
    tracker_mocker = mocker.patch.object(Tracker, "__init__", return_value=None)
    tracker_sync_mocker = mocker.patch.object(Tracker, "sync")

    call_command("syncproject", project.name)

    tracker_mocker.assert_called_once_with(project)
    tracker_sync_mocker.assert_called_once()


@pytest.mark.django_db(transaction=True)
def test_syncprojects(project_factory, mocker):
    tracker_mocker = mocker.patch.object(Tracker, "__init__", return_value=None)
    tracker_sync_mocker = mocker.patch.object(Tracker, "sync")

    projects = project_factory.create_batch(5)

    call_command("syncprojects")

    tracker_mocker.assert_has_calls(
        [call(project) for project in projects],
        any_order=True,
    )

    assert tracker_sync_mocker.call_count == 5
