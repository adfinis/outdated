from django.conf import settings
from requests import get
from watchman.decorators import check


@check
def _oidc_check():
    well_known = (
        settings.OIDC_OP_BASE_ENDPOINT.removesuffix("protocol/openid-connect")
        + ".well-known/openid-configuration"
    )
    resp = get(well_known, timeout=10, verify=settings.OIDC_VERIFY_SSL)
    resp.raise_for_status()
    return {"ok": True}


def oidc():
    return {"oidc-configuration": _oidc_check()}
