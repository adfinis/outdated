from datetime import datetime

import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient

from .outdated import factories

register(factories.DependencyFactory)
register(factories.DependencyVersionFactory)
register(factories.ProjectFactory)


@pytest.fixture
def client(db):
    """Return rest framework client, includes db."""
    return APIClient()


@pytest.fixture
def format_date():
    def _format_date(date: str):
        return datetime.strptime(date, "%Y-%m-%d").date()

    return _format_date
