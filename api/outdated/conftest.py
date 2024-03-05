from __future__ import annotations

from functools import partial
from typing import TYPE_CHECKING

import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient

from .oidc_auth.models import OIDCUser
from .outdated import factories
from .outdated.tracking import Tracker
from .user.factories import UserFactory

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path
    from unittest.mock import MagicMock

    from pytest_django.fixtures import SettingsWrapper
    from pytest_mock import MockerFixture


register(factories.DependencyFactory)
register(factories.VersionFactory)
register(factories.ReleaseVersionFactory)
register(factories.ProjectFactory)
register(factories.MaintainerFactory)
register(UserFactory)


def _get_claims(
    settings: SettingsWrapper,
    id_claim: str = "00000000-0000-0000-0000-000000000000",
    groups_claim: list | None = None,
    email_claim: str = "test@example.com",
    first_name_claim: str = "foo",
    last_name_claim: str = "bar",
    username_claim: str = "foobar",
) -> dict[str]:
    groups_claim = groups_claim if groups_claim else []
    return {
        settings.OIDC_CLAIMS["ID"]: id_claim,
        settings.OIDC_CLAIMS["GROUPS"]: groups_claim,
        settings.OIDC_CLAIMS["EMAIL"]: email_claim,
        settings.OIDC_CLAIMS["FIRST_NAME"]: first_name_claim,
        settings.OIDC_CLAIMS["LAST_NAME"]: last_name_claim,
        settings.OIDC_CLAIMS["USERNAME"]: username_claim,
    }


@pytest.fixture
def get_claims(settings: SettingsWrapper) -> partial[dict]:
    return partial(_get_claims, settings)


@pytest.fixture
def claims(settings: SettingsWrapper) -> dict[str]:
    return _get_claims(settings)


def _get_client(user: OIDCUser) -> APIClient:
    client = APIClient()
    client.force_authenticate(user=user)
    client.user = user
    return client


@pytest.fixture
def client(db, settings, get_claims) -> APIClient:  # noqa: ANN001
    """Return rest framework client, includes db."""
    user = OIDCUser(
        "sometoken",
        get_claims(id_claim="user", groups_claim=[], email_claim="user@example.com"),
    )
    return _get_client(user)


@pytest.fixture
def admin_client(db, settings, get_claims) -> APIClient:  # noqa: ANN001
    """Return rest framework client with admin privileges, includes db."""
    user = OIDCUser(
        "sometoken",
        get_claims(
            id_claim="admin",
            username_claim="admin",
            groups_claim=[settings.OIDC_ADMIN_GROUP],
            email_claim="admin@example.com",
        ),
    )
    return _get_client(user)


@pytest.fixture
def tracker_mock(mocker: MockerFixture) -> Callable[[str], MagicMock]:
    """
    Generate mock for Tracker.

    Example:
    -------
        ```
        def test_tracker_thing(project, tracker_mock):
            tracker_sync_mock = tracker_mock('sync')
            Tracker(project).sync()
            tracker_sync_mock.assert_called_once()
        ```

    """

    def _tracker_mock(target: str) -> MagicMock:
        return mocker.patch.object(Tracker, target)

    return _tracker_mock


@pytest.fixture
def tracker_init_mock(mocker: MockerFixture) -> MagicMock:
    """Mock for the Trackers __init__ method."""
    return mocker.patch.object(Tracker, "__init__", return_value=None)


@pytest.fixture
def tmp_repo_root(settings: SettingsWrapper, tmp_path: Path) -> Path:
    """Change settings.REPOSITORY_ROOT to a temporary directory."""
    settings.REPOSITORY_ROOT = str(tmp_path.absolute())
    return tmp_path
