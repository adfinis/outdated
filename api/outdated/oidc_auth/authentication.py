from django.conf import settings
from django.core.exceptions import SuspiciousOperation
from mozilla_django_oidc.auth import OIDCAuthenticationBackend

from .models import OIDCUser


class OutdatedOIDCAuthenticationBackend(OIDCAuthenticationBackend):
    def verify_claims(self, claims):
        claims_to_verify = [
            settings.OIDC_CLAIMS["ID"],
            settings.OIDC_CLAIMS["EMAIL"],
            settings.OIDC_CLAIMS["GROUPS"],
        ]

        for claim in claims_to_verify:
            if claim not in claims:
                msg = f'Couldn\'t find "{claim}" claim'
                raise SuspiciousOperation(msg)

    def get_or_create_user(self, access_token, *args):
        claims = self.get_userinfo(access_token, *args)

        self.verify_claims(claims)

        return OIDCUser(access_token, claims)
