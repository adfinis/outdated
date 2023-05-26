from functools import partial

import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient

from outdated.oidc_auth.models import OIDCUser

from .outdated import factories
from .user.factories import UserFactory

register(factories.DependencyFactory)
register(factories.VersionFactory)
register(factories.ReleaseVersionFactory)
register(factories.ProjectFactory)
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


@pytest.fixture(scope="module")
def vcr_config():
    return {
        # Replace the Authorization header with a dummy value
        "filter_headers": [("Authorization", "DUMMY")],
        "ignore_localhost": True,
        "ignore_hosts": ["https://outdated.local"],
    }
