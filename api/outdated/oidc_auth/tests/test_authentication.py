import json

import pytest
from mozilla_django_oidc.contrib.drf import OIDCAuthentication
from requests.exceptions import HTTPError
from rest_framework import exceptions, status
from rest_framework.exceptions import AuthenticationFailed

from outdated.oidc_auth.models import OIDCUser
from outdated.user.models import User


@pytest.mark.parametrize(
    "authentication_header,authenticated,error",
    [
        ("", False, False),
        ("Bearer", False, True),
        ("Bearer Too many params", False, True),
        ("Basic Auth", False, True),
        ("Bearer Token", True, False),
    ],
)
def test_authentication(
    db, rf, authentication_header, authenticated, error, requests_mock, settings, claims
):
    assert User.objects.count() == 0

    requests_mock.get(settings.OIDC_OP_USER_ENDPOINT, text=json.dumps(claims))

    request = rf.get("/openid", HTTP_AUTHORIZATION=authentication_header)

    try:
        result = OIDCAuthentication().authenticate(request)
    except exceptions.AuthenticationFailed:
        assert error
        return
    if authenticated:
        oidc_user, auth = result
        assert oidc_user.is_authenticated
        assert auth == authentication_header.split(" ")[1]
        assert User.objects.count() == 1
    else:
        assert result is None


@pytest.mark.parametrize(
    "modified_claim", ["email", "first_name", "last_name", "username"]
)
def test_authentication_claims_changed(
    db,
    rf,
    requests_mock,
    settings,
    get_claims,
    modified_claim,
):
    user = OIDCUser("sometoken", get_claims()).user
    claims = get_claims(**{modified_claim + "_claim": "modified"})
    requests_mock.get(settings.OIDC_OP_USER_ENDPOINT, text=json.dumps(claims))
    request = rf.get("/openid", HTTP_AUTHORIZATION="Bearer Token")

    modified_user = OIDCAuthentication().authenticate(request)[0].user
    assert User.objects.count() == 1
    assert getattr(user, modified_claim) != getattr(modified_user, modified_claim)


def test_authentication_idp_502(
    db,
    rf,
    requests_mock,
    settings,
):
    requests_mock.get(
        settings.OIDC_OP_USER_ENDPOINT, status_code=status.HTTP_502_BAD_GATEWAY
    )

    request = rf.get("/openid", HTTP_AUTHORIZATION="Bearer Token")
    with pytest.raises(HTTPError):
        OIDCAuthentication().authenticate(request)


def test_authentication_idp_missing_claim(
    db,
    rf,
    requests_mock,
    settings,
    claims,
):
    settings.OIDC_CLAIMS["ID"] = "missing"
    requests_mock.get(settings.OIDC_OP_USER_ENDPOINT, text=json.dumps(claims))

    request = rf.get("/openid", HTTP_AUTHORIZATION="Bearer Token")
    with pytest.raises(AuthenticationFailed):
        OIDCAuthentication().authenticate(request)
