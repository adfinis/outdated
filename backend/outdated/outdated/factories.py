import random
from datetime import date, timedelta

from factory import Faker, Sequence, SubFactory, Trait, post_generation
from factory.django import DjangoModelFactory

from . import models


class DependencyFactory(DjangoModelFactory):
    name = Faker("uuid4")

    class Meta:
        model = models.Dependency


class DependencyVersionFactory(DjangoModelFactory):
    class Meta:
        model = models.DependencyVersion

    dependency = SubFactory(DependencyFactory)
    version = ".".join([str(random.randint(0, 9)) for _ in range(3)])
    release_date = Faker(
        "date_between_dates",
        date_start=date.today() - timedelta(days=80),
        date_end=date.today(),
    )
    eol_date = Faker(
        "date_between_dates",
        date_start=release_date,
        date_end=date.today() + timedelta(days=80),
    )

    class Params:
        outdated = Trait(eol_date=date.today() - timedelta(days=80))
        warning = Trait(eol_date=date.today() + timedelta(days=20))
        up_to_date = Trait(eol_date=date.today() + timedelta(days=31))


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
