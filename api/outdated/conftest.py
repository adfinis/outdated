import pytest
from django.contrib.auth.models import User
from pytest_factoryboy import register
from rest_framework.test import APIClient

from .outdated import factories

register(factories.DependencyFactory)
register(factories.VersionFactory)
register(factories.ReleaseVersionFactory)
register(factories.ProjectFactory)


@pytest.fixture
def client(db, settings):
    """Return rest framework client, includes db."""
    client = APIClient()
    user = User(
        "sometoken",
        {settings.OIDC_ID_CLAIM: "user", settings.OIDC_EMAIL_CLAIM: "test@example.com"},
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
