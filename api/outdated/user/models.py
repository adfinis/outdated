from django.db import models

from outdated.models import UUIDModel


class User(UUIDModel):
    idp_id = models.CharField(max_length=255, unique=True, null=True, blank=False)
    first_name = models.CharField(max_length=150, null=True)
    last_name = models.CharField(max_length=150, null=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, unique=True, null=True)

    def __str__(self) -> str:
        return self.username or self.email
