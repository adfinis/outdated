from __future__ import annotations

from typing import TYPE_CHECKING, Literal

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

if TYPE_CHECKING:
    from outdated.user.models import User

METHODS = [
    (APIClient.get, "list", None),
    (APIClient.get, "detailed", None),
    (APIClient.options, "list", None),
    (APIClient.head, "list", None),
    (APIClient.post, "list", {}),
    (APIClient.patch, "detailed", {}),
    (APIClient.delete, "detailed", None),
]

SAFE_METHODS = (APIClient.get, APIClient.options, APIClient.head)


@pytest.mark.parametrize("method,request_type,data", METHODS)
@pytest.mark.parametrize("is_admin", [True, False])
def test_readonly(
    admin_client: APIClient,
    client: APIClient,
    user: User,
    is_admin: bool,
    method: APIClient.get
    | APIClient.options
    | APIClient.head
    | APIClient.post
    | APIClient.patch
    | APIClient.delete,
    request_type: Literal["list", "detailed"],
    data: dict | None,
) -> None:
    api_client = admin_client if is_admin else client

    url = (
        reverse("user-detail", args=[user.id])
        if request_type == "detailed"
        else reverse("user-list")
    )

    response = method(api_client, url, data=data)
    if method in SAFE_METHODS:
        assert response.status_code != 403
    else:
        assert (response.status_code != 403) == is_admin
