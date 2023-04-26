import random
from datetime import date, timedelta

from factory import Faker, Sequence, SubFactory, Trait, post_generation
from factory.django import DjangoModelFactory

from . import models

DEPENDENCIES = [
    ("django", "PIP"),
    ("djangorestframework", "PIP"),
    ("djangorestframework-jsonapi", "PIP"),
    ("django-filter", "PIP"),
    ("django-cors-headers", "PIP"),
    ("django-extensions", "PIP"),
    ("django-debug-toolbar", "PIP"),
    ("django-environ", "PIP"),
    ("flake8", "PIP"),
    ("flake8-bugbear", "PIP"),
    ("flake8-tuple", "PIP"),
    ("flake8-isort", "PIP"),
    ("flake8-debugger", "PIP"),
    ("pytest", "PIP"),
    ("pytest-django", "PIP"),
    ("pytest-cov", "PIP"),
    ("pytest-vcr", "PIP"),
    ("pytest-factoryboy", "PIP"),
    ("python-dateutil", "PIP"),
    ("ember-source", "NPM"),
    ("ember-cli", "NPM"),
    ("ember-data", "NPM"),
    ("ember-cli-htmlbars", "NPM"),
    ("ember-cli-htmlbars-inline-precompile", "NPM"),
    ("ember-cli-babel", "NPM"),
    ("ember-cli-qunit", "NPM"),
    ("@glimmer/component", "NPM"),
    ("@glimmer/tracking", "NPM"),
]


class DependencyFactory(DjangoModelFactory):
    name, provider = random.choice(DEPENDENCIES)

    class Meta:
        model = models.Dependency


class ReleaseVersionFactory(DjangoModelFactory):
    class Meta:
        model = models.ReleaseVersion

    dependency = SubFactory(DependencyFactory)
    version = ".".join([str(random.randint(0, 9)) for _ in range(3)])
    release_date = Faker(
        "date_between_dates",
        date_start=date.today() - timedelta(days=80),
        date_end=date.today(),
    )

    class Params:
        undefined = Trait(release_date=None)
        outdated = Trait(version="0.0.0")
        warning = Trait(
            version="4.2.0",
            release_date=date.today() - timedelta(days=365),
            dependency=SubFactory(
                DependencyFactory,
                name="django",
                provider="PIP",
            ),
        )
        up_to_date = Trait(
            version="4.2.0",
            release_date=date.today(),
            dependency=SubFactory(
                DependencyFactory,
                name="django",
                provider="PIP",
            ),
        )


class VersionFactory(DjangoModelFactory):
    class Meta:
        model = models.Version


class ProjectFactory(DjangoModelFactory):
    name = Faker("uuid4")
    repo = Sequence(lambda n: "https://github.com/userorcompany/%s/" % n)

    @post_generation
    def dependency_versions(self, create, extracted, **kwargs):
        if not create:
            return  # pragma: no cover
        if extracted:
            for dependency_version in extracted:
                self.dependency_versions.add(dependency_version)

    class Meta:
        model = models.Project
