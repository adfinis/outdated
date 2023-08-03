from datetime import date, timedelta
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from .. import models


@pytest.mark.parametrize(
    "status,called",
    (["UNDEFINED", False], ["OUTDATED", True], ["WARNING", True], ["UP-TO-DATE", True]),
)
def test_build_notification_queue_called(
    transactional_db,
    mocker: MockerFixture,
    status,
    called,
    project_factory,
    release_version_factory,
    version_factory,
):
    build_notification_queue_mock: MagicMock = mocker.patch.object(
        models, "build_notification_queue"
    )
    release_version = release_version_factory(
        undefined=status == "UNDEFINED",
        outdated=status == "OUTDATED",
        warning=status == "WARNING",
        up_to_date=status == "UP-TO-DATE",
    )
    version = version_factory(release_version=release_version)
    project = project_factory()
    assert build_notification_queue_mock.call_count == 0
    project.versioned_dependencies.add(version)

    if called:
        build_notification_queue_mock.assert_called_with(project)
        other_project = project_factory(versioned_dependencies=[version])
        build_notification_queue_mock.assert_called_with(other_project)

        release_version.end_of_life = date.today() + timedelta(days=2000)
        release_version.save()

        assert build_notification_queue_mock.call_count == 4
    else:
        assert build_notification_queue_mock.call_count == 0
