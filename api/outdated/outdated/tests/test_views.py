from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import pytest

from outdated.oidc_auth.models import OIDCUser  # noqa: TCH001
from outdated.outdated.serializers import (
    ReleaseVersionLimitedSerializer,
    ReleaseVersionSerializer,
)
from outdated.outdated.views import ReleaseVersionViewSet

if TYPE_CHECKING:
    from rest_framework.test import APIClient


@dataclass
class Request:
    user: OIDCUser


@pytest.mark.parametrize("is_admin", [True, False])
def test_release_version_serializer(
    client: APIClient, admin_client: APIClient, is_admin: bool
) -> None:
    api_client = admin_client if is_admin else client

    serializer = ReleaseVersionViewSet(
        request=Request(api_client.user)
    ).get_serializer_class()

    if is_admin:
        assert serializer == ReleaseVersionSerializer
    else:
        assert serializer == ReleaseVersionLimitedSerializer
