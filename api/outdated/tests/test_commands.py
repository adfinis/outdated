from unittest.mock import call

import pytest

from outdated.commands import ProjectCommand


@pytest.mark.parametrize("all_projects", [True, False])
def test_command_handle(transactional_db, project_factory, all_projects, mocker):
    projects = project_factory.create_batch(5)
    argv = ["", "project-command-test"]
    handle_mock = mocker.patch.object(ProjectCommand, "_handle")
    ProjectCommand().run_from_argv(
        [*argv, *(["--all"] if all else [project.name for project in projects])],
    )
    handle_mock.assert_has_calls(
        [call(project) for project in projects],
        any_order=True,
    )


@pytest.mark.parametrize(
    "existing_projects",
    [
        [],
        ["foo"],
        ["Foo"],
        ["foo", "foobar"],
    ],
)
@pytest.mark.parametrize("nonexistant_projects", [["bar"], ["baz", "bar"]])
def test_project_command(
    transactional_db,
    project_factory,
    capsys,
    nonexistant_projects,
    existing_projects,
):
    argv = ["", "project-command-test"]
    for project in existing_projects:
        project_factory(name=project)
    ProjectCommand().run_from_argv([*argv, *nonexistant_projects, *existing_projects])
    _, stderr = capsys.readouterr()
    nonexistant_projects.sort()
    assert (
        stderr
        == f"Projects with names {', '.join(nonexistant_projects)} do not exist\n"
    )
