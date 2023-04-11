from django.core.management import call_command
from time import sleep
from outdated.outdated.models import Project


def test_syncproject(db, project_factory):
    project = project_factory.create(repo="https://github.com/adfinis/outdated")
    assert project.dependency_versions.count() == 0
    call_command("syncproject", "project-does-not-exist")
    assert project.dependency_versions.count() == 0
    call_command("syncproject", project.name)
    assert Project.objects.get(name=project.name).dependency_versions.count() > 0
