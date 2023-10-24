from django.core.management import call_command

from outdated.notifications.notifier import Notifier


def test_notify(
    db,
    project,
    maintainer_factory,
    version_factory,
    release_version_factory,
    capsys,
    mocker,
):
    call_command("notify", project.name)
    stdout, _ = capsys.readouterr()
    assert stdout == f"Skipped {project.name} (no-maintainers)\n"
    maintainer_factory(project=project)
    call_command("notify", project.name)
    notify_mocker = mocker.spy(Notifier, "__init__")
    stdout, _ = capsys.readouterr()
    assert stdout == ""
    notify_mocker.assert_not_called()
    project.versioned_dependencies.set(
        [version_factory(release_version=release_version_factory(warning=True))]
    )
    project.save()
    call_command("notify", project.name)
    notify_mocker.assert_called_once()
