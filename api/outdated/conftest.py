from datetime import datetime

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


@pytest.fixture
def str_to_date():
    """Convert a string to a date."""

    def _str_to_date(date):
        if date:
            return datetime.strptime(date, "%Y-%m-%d").date()
        return None  # pragma: no cover

    return _str_to_date


@pytest.fixture(scope="module")
def vcr_config():
    return {
        # Replace the Authorization header with a dummy value
        "filter_headers": [("Authorization", "DUMMY")],
        "ignore_localhost": True,
    }
