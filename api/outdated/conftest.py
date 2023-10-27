from __future__ import annotations

from collections.abc import Callable
from functools import partial
from unittest.mock import MagicMock

import pytest
from pytest_factoryboy import register
from pytest_mock import MockerFixture
from rest_framework.test import APIClient

from .oidc_auth.models import OIDCUser
from .outdated import factories
from .tracking import Tracker
from .user.factories import UserFactory

register(factories.DependencyFactory)
register(factories.VersionFactory)
register(factories.ReleaseVersionFactory)
register(factories.ProjectFactory)
register(factories.MaintainerFactory)
register(UserFactory)


def _get_claims(
    settings,
    id_claim="00000000-0000-0000-0000-000000000000",
    groups_claim=None,
    email_claim="test@example.com",
    first_name_claim="foo",
    last_name_claim="bar",
    username_claim="foobar",
):
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
def get_claims(settings):
    return partial(_get_claims, settings)


@pytest.fixture
def claims(settings):
    return _get_claims(settings)


@pytest.fixture
def client(db, settings, get_claims):
    """Return rest framework client, includes db."""
    client = APIClient()
    user = OIDCUser(
        "sometoken",
        get_claims(id_claim="user", groups_claim=[], email_claim="user@example.com"),
    )
    client.force_authenticate(user=user)
    client.user = user
    return client


@pytest.fixture
def tracker_mock(mocker: MockerFixture) -> Callable[[str], MagicMock]:
    def _tracker_mock(target: str) -> MagicMock:
        return mocker.patch.object(Tracker, target)

    return _tracker_mock


@pytest.fixture
def tracker_init_mock(mocker: MockerFixture) -> MagicMock:
    return mocker.patch.object(Tracker, "__init__", return_value=None)
