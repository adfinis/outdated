import datetime
import random

from factory import Faker, Sequence, SubFactory, post_generation
from factory.django import DjangoModelFactory

from . import models


class DependencyFactory(DjangoModelFactory):
    name = Faker("uuid4")

    class Meta:
        model = models.Dependency


class DependencyVersionFactory(DjangoModelFactory):

    dependency = SubFactory(DependencyFactory)
    version = ".".join([str(random.randint(0, 9)) for _ in range(3)])
    release_date = Faker(
        "date_between_dates",
        date_start=datetime.date.today() - datetime.timedelta(80),
        date_end=datetime.date.today(),
    )
    eol_date = Faker(
        "date_between_dates",
        date_start=release_date,
        date_end=datetime.date.today() + datetime.timedelta(80),
    )

    class Meta:
        model = models.DependencyVersion


class ProjectFactory(DjangoModelFactory):
    name = Faker("uuid4")
    repo = Sequence(lambda n: "https://github.com/userorcompany/%s/" % n)

    @post_generation
    def dependency_versions(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.dependency_versions.add(*extracted)

    class Meta:
        model = models.Project
