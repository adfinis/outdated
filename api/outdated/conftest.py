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
def str_to_date():
    def _str_to_date(date):
        if date:
            return datetime.strptime(date, "%Y-%m-%d").date()
        return None

    return _str_to_date


@pytest.fixture
def get_sample():
    def _get_sample(name):
        return open(f"outdated/outdated/tests/samples/{name}").read()

    return _get_sample
