import random
from datetime import date, timedelta

from factory import Faker, Sequence, SubFactory, Trait, post_generation
from factory.django import DjangoModelFactory

from ..user.factories import UserFactory
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
    end_of_life = Faker("date_this_year")
    major_version = random.randint(0, 10)
    minor_version = random.randint(0, 10)

    class Params:
        undefined = Trait(end_of_life=None)
        outdated = Trait(end_of_life=date.today())
        warning = Trait(
            end_of_life=date.today() + timedelta(days=150),
        )
        up_to_date = Trait(
            end_of_life=date.today() + timedelta(days=365),
        )


class VersionFactory(DjangoModelFactory):
    release_version = SubFactory(ReleaseVersionFactory)
    patch_version = random.randint(0, 28)
    release_date = Faker("date_this_year")

    class Meta:
        model = models.Version


class ProjectFactory(DjangoModelFactory):
    name = Faker("uuid4")
    repo = Sequence(lambda n: "https://github.com/userorcompany/%s/" % n)

    @post_generation
    def versioned_dependencies(self, create, extracted, **kwargs):
        if not create:
            return  # pragma: no cover
        if extracted:
            for versioned_dependency in extracted:
                self.versioned_dependencies.add(versioned_dependency)

    class Meta:
        model = models.Project


class MaintainerFactory(DjangoModelFactory):
    project = SubFactory(ProjectFactory)
    user = SubFactory(UserFactory)

    class Meta:
        model = models.Maintainer
