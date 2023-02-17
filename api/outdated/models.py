from uuid import uuid4

from django.db import models


class UUIDModel(models.Model):
    """Model which uses an uuid as primary key."""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    class Meta:
        abstract = True
