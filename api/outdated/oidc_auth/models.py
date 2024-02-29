from django.conf import settings

from outdated.user.models import User


class BaseUser:  # pragma: no cover
    def __init__(self):
        self.email = None
        self.groups = []
        self.group = None
        self.token = None
        self.claims = {}
        self.is_authenticated = False

    def __str__(self):
        raise NotImplementedError


class OIDCUser(BaseUser):
    def __init__(self, token: str, claims: dict) -> None:
        super().__init__()

        self.claims = claims
        self.id = self.claims[settings.OIDC_CLAIMS["ID"]]
        self.email = self.claims.get(settings.OIDC_CLAIMS["EMAIL"])
        self.groups = self.claims.get(settings.OIDC_CLAIMS["GROUPS"], [])
        self.group = self.groups[0] if self.groups else None
        self.first_name = self.claims.get(settings.OIDC_CLAIMS["FIRST_NAME"])
        self.last_name = self.claims.get(settings.OIDC_CLAIMS["LAST_NAME"])
        self.username = self.claims.get(settings.OIDC_CLAIMS["USERNAME"])

        self.token = token
        self.is_authenticated = True
        self.user = self._get_or_create_user()

    def _get_or_create_user(self):
        user, _ = User.objects.update_or_create(
            idp_id=self.id,
            defaults={
                "email": self.email,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "username": self.username,
            },
        )
        return user

    @property
    def is_admin(self):
        return settings.OIDC_ADMIN_GROUP in self.groups

    def __str__(self):
        return f"{self.email} - {self.id}"
