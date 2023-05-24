from uuid import uuid4

from factory import Faker
from factory.django import DjangoModelFactory

from . import models


class UserFactory(DjangoModelFactory):
    """User factory."""

    first_name = Faker("first_name")
    last_name = Faker("last_name")
    email = Faker("email")
    username = Faker("user_name")
    idp_id = uuid4()

    class Meta:
        """Meta informations for the user factory."""

        model = models.User
