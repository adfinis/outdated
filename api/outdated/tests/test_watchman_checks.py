from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from django.urls import reverse

if TYPE_CHECKING:
    from pytest_django.fixtures import SettingsWrapper
    from requests_mock import Mocker
    from rest_framework.test import APIClient


@pytest.mark.parametrize(
    "status_code,success",
    [
        (200, True),
        (404, False),
        (502, False),
        (503, False),
    ],
)
def test_oidc_check(
    status_code: int,
    success: bool,
    requests_mock: Mocker,
    settings: SettingsWrapper,
    client: APIClient,
) -> None:
    settings.OIDC_OP_BASE_ENDPOINT = (
        "https://login.outdated.example/realms/outdated/protocol/openid-connect"
    )
    requests_mock.get(
        "https://login.outdated.example/realms/outdated/.well-known/openid-configuration",
        status_code=status_code,
    )

    url = reverse("health")

    resp = client.get(url)

    assert (resp.status_code != settings.WATCHMAN_ERROR_CODE) == success
