from django.core.management import call_command


def test_syncproject(mocked_project):
    project = mocked_project

    call_command("syncproject", "a-project-that-does-not-exist")

    assert project.dependency_versions.count() == 0

    call_command("syncproject", project.name)

    assert project.dependency_versions.count() == 1
