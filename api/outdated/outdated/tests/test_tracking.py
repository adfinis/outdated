from unittest.mock import PropertyMock, call

import pytest
from django.conf import settings
from django.urls import reverse
from rest_framework import status

from outdated.outdated import tracking
from outdated.outdated.models import Project
from outdated.outdated.parser import LockfileParser
from outdated.outdated.tracking import RepoError, Tracker


@pytest.mark.parametrize(
    "repo,repo_type,reinitialize",
    [
        ("github.com/Adfinis/Outdated", "public", False),
        ("github.com/adfinis/outdated", "access-token", False),
        ("Github.Com/ADFINIS/OutdAted", "public", False),
        ("github.com/adfinis/mysagw", "public", True),
        ("github.com/adfinis/timed-frontend", "public", True),
        ("github.com/adfinis/timed-backend", "public", True),
    ],
)
def test_serializer_patch(
    client,
    project_factory,
    tracker_init_mock,
    tracker_mock,
    repo,
    reinitialize,
    repo_type,
    settings,
):
    project = project_factory(repo="github.com/adfinis/outdated", repo_type=repo_type)
    setup_mock = tracker_mock("setup")
    delete_mock = tracker_mock("delete")

    settings.VALIDATE_REMOTES = False

    data = {
        "data": {
            "type": "projects",
            "id": project.id,
            "attributes": {
                "name": project.name,
                "repo": repo,
                "repo_type": repo_type,
            },
            "relationships": {},
        },
    }

    if repo_type == "access-token":
        data["data"]["attributes"]["access_token"] = "token"  # noqa: S105

    url = reverse("project-detail", args=[project.id])

    resp = client.patch(url, data)
    assert resp.status_code == status.HTTP_200_OK

    if reinitialize:
        delete_mock.assert_called_once()
        setup_mock.assert_called_once()
        assert tracker_init_mock.call_count == 2
        assert (
            tracker_init_mock.call_args_list[0].args[0].repo
            == "github.com/adfinis/outdated"
        )
        tracker_init_mock.assert_called_with(
            project, "token" if repo_type == "access-token" else None
        )
    else:
        delete_mock.assert_not_called()
        setup_mock.assert_not_called()
        tracker_init_mock.assert_not_called()


@pytest.mark.parametrize("access_token", [None, "token"])
def test_serializer_create(
    client, tracker_init_mock, tracker_mock, settings, access_token
):
    setup_mock = tracker_mock("setup")

    # don't depend on github
    settings.VALIDATE_REMOTES = False

    data = {
        "data": {
            "type": "projects",
            "id": None,
            "attributes": {
                "name": "foo",
                "repo": "github.com/adfinis/outdated",
                "repo_type": "access-token" if access_token else "public",
            },
            "relationships": {},
        },
    }

    if access_token:
        data["data"]["attributes"]["access_token"] = access_token

    url = reverse("project-list")

    response = client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    project = Project.objects.get(name="foo")
    tracker_init_mock.assert_called_once_with(project, access_token)
    setup_mock.assert_called_once()


def test_view_delete(client, project, tracker_init_mock, tracker_mock):
    delete_mock = tracker_mock("delete")
    url = reverse("project-detail", args=[project.id])
    resp = client.delete(url)
    assert resp.status_code == status.HTTP_204_NO_CONTENT
    tracker_init_mock.assert_called_once()
    delete_mock.assert_called_once()
    assert not Project.objects.filter(id=project.id)


@pytest.mark.parametrize("access_token", [None, "token"])
def test_clone(db, project_factory, tmp_repo_root, tracker_mock, access_token):
    tracker_run_mock = tracker_mock("_run")
    tracker_delete_mock = tracker_mock("delete")
    project: Project = project_factory(
        repo="github.com/adfinis/outdated",
        repo_type="access-token" if access_token else "public",
    )

    tracker = Tracker(project, access_token)

    tracker.clone()

    tracker_run_mock.assert_has_calls(
        [
            call(
                [
                    "git",
                    "clone",
                    "-n",
                    "--depth=1",
                    "--filter=tree:0",
                    "--single-branch",
                    "https://outdated:token@github.com/adfinis/outdated"
                    if access_token
                    else "https://github.com/adfinis/outdated",
                    tmp_repo_root / "github.com/adfinis/outdated",
                ],
            ),
            call(
                [
                    "git",
                    "sparse-checkout",
                    "set",
                    "--no-cone",
                    *settings.SUPPORTED_LOCK_FILES,
                ],
            ),
        ],
    )

    tracker_delete_mock.assert_called_once()


@pytest.mark.parametrize("requires_local_copy", [True, False])
@pytest.mark.parametrize("exists", [True, False])
def test_run(
    db,
    project,
    tmp_repo_root,
    requires_local_copy,
    exists,
    mocker,
):
    project_path = tmp_repo_root / project.clone_path

    subprocess_run_mock = mocker.patch.object(tracking, "run")

    assert not project_path.exists()

    if exists:
        project_path.mkdir(parents=True, exist_ok=False)

    tracker = Tracker(project)

    assert tracker.local_path == project_path

    try:
        tracker._run([], requires_local_copy)  # noqa: SLF001
        if not exists:
            assert not requires_local_copy
        if requires_local_copy:
            assert exists
        subprocess_run_mock.assert_called_once_with(
            [],
            cwd=(project_path if exists else tmp_repo_root),
            capture_output=True,
            check=False,
        )
    except RepoError:
        assert not exists
        assert requires_local_copy
        subprocess_run_mock.assert_not_called()


@pytest.mark.parametrize("exists", [True, False])
def test_sync(
    db,
    project,
    tmp_repo_root,
    tracker_mock,
    exists,
    mocker,
    version_factory,
):
    project_path = tmp_repo_root / project.clone_path

    tracker_clone_mock = tracker_mock("clone")
    tracker_checkout_mock = tracker_mock("checkout")

    tracker_lockfile_mock = mocker.patch(
        "outdated.outdated.tracking.Tracker.lockfiles",
        return_value=[],
        new_callable=PropertyMock,
    )

    lockfile_parser_init_mock = mocker.patch.object(
        LockfileParser,
        "__init__",
        return_value=None,
    )

    versions = version_factory.create_batch(5)
    lockfile_parser_parser_mock = mocker.patch.object(
        LockfileParser,
        "parse",
        return_value=versions,
    )

    tracker = Tracker(project)
    assert tracker.local_path == project_path
    assert not project.versioned_dependencies.all()
    if exists:
        project_path.mkdir(parents=True, exist_ok=False)

    tracker.sync()

    if exists:
        tracker_clone_mock.assert_not_called()
    else:
        tracker_clone_mock.assert_called_once()

    tracker_checkout_mock.assert_called_once()

    lockfile_parser_init_mock.assert_called_once_with([])

    lockfile_parser_parser_mock.assert_called_once_with()

    tracker_lockfile_mock.assert_called_once()

    assert set(project.versioned_dependencies.all()) == set(versions)


@pytest.mark.parametrize("exists", [True, False])
def test_lockfiles(db, project, tmp_repo_root, exists):
    tracker = Tracker(project)

    if exists:
        tracker.local_path.mkdir(parents=True, exist_ok=False)
        git_dir = tracker.local_path / ".git"
        git_dir.mkdir(exist_ok=False)

    try:
        lockfiles = tracker.lockfiles
        assert exists
        assert lockfiles == []
        poetry_lock = tracker.local_path / "poetry.lock"
        poetry_lock.write_text("")
        assert tracker.lockfiles == [poetry_lock]
    except RepoError:
        assert not exists
