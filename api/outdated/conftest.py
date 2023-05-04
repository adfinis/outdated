import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient

from .outdated import factories

register(factories.DependencyFactory)
register(factories.VersionFactory)
register(factories.ReleaseVersionFactory)
register(factories.ProjectFactory)


@pytest.fixture
def client(db):
    """Return rest framework client, includes db."""
    return APIClient()
