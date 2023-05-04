import pytest
from django.core.management import call_command


@pytest.mark.vcr()
@pytest.mark.django_db(transaction=True)
def test_syncproject(project_factory):
    call_command("syncproject", "foo")

    project = project_factory.create(repo="https://github.com/projectcaluma/caluma")

    call_command("syncproject", project.name)
    assert project.versioned_dependencies.count() > 0


@pytest.mark.vcr()
@pytest.mark.django_db(transaction=True)
def test_syncprojects(project_factory):
    projects = [
        project_factory(repo=f"https://github.com/adfinis/{project}")
        for project in ["outdated", "mysagw"]
    ]

    call_command("syncprojects")
    for project in projects:
        assert project.versioned_dependencies.count() > 0
