from datetime import datetime
from json import loads
from re import compile

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
    """Convert a string to a date."""

    def _str_to_date(date):
        if date:
            return datetime.strptime(date, "%Y-%m-%d").date()
        return None

    return _str_to_date


@pytest.fixture
def get_sample():
    """Get a sample file."""

    def _get_sample(name):
        return open(f"outdated/outdated/tests/samples/{name}").read()

    return _get_sample


@pytest.fixture
def mocked_project(db, requests_mock, get_sample, project_factory):
    """Return a mocked project."""
    project = project_factory.create(repo="https://github.com/adfinis/outdated")
    yarn_lock_url = (
        "https://api.github.com/repositories/560760559/contents/frontend/yarn.lock"
    )

    requests_mock.get(
        compile(r"https:\/\/api\.github\.com\/search\/code.*"),
        json={"items": [{"url": yarn_lock_url}]},
    )

    yarn_lock_download_url = "https://raw.githubusercontent.com/adfinis/Outdated/f4dafa49a0c0357214647e7cd79dcd0aad811a91/frontend/yarn.lock"

    requests_mock.get(
        yarn_lock_url,
        json={
            "download_url": yarn_lock_download_url,
        },
    )

    requests_mock.get(
        yarn_lock_download_url,
        text=get_sample("lockfiles/yarn"),
    )

    requests_mock.get(
        "https://registry.npmjs.org/ember-cli",
        json=loads(get_sample("release-dates/yarn.json"))["response"],
    )
    return project
