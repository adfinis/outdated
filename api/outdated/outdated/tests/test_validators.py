from __future__ import annotations

from contextlib import suppress
from subprocess import run
from typing import TYPE_CHECKING
from unittest.mock import call

import pytest
from django.core.exceptions import ValidationError

from outdated.outdated import validators
from outdated.outdated.serializers import ProjectSerializer

if TYPE_CHECKING:
    from pathlib import Path
    from typing import Literal

    from pytest_mock import MockerFixture

    from outdated.outdated.factories import ProjectFactory
    from outdated.outdated.models import Project

type RepoType = Literal["public", "access-token"]


@pytest.mark.django_db()
@pytest.mark.parametrize("access_token", [None, "token"])
@pytest.mark.parametrize("repo_type", ["public", "access-token"])
@pytest.mark.parametrize("instance", [True, False])
def test_access_token_required(
    repo_type: RepoType, access_token: None | str, instance: bool, project: Project
) -> None:
    attrs = {
        "repo_type": repo_type,
        "access_token": access_token,
    }

    serializer = ProjectSerializer(project if instance else None)

    try:
        validators.validate_access_token_required(attrs, serializer)
        if repo_type == "access-token" and not access_token:
            assert serializer.instance
        elif repo_type == "access-token":
            assert access_token
        else:
            assert repo_type == "public"

    except ValidationError:
        assert repo_type == "access-token"
        assert not access_token


@pytest.mark.parametrize("access_token", [None, "token"])
@pytest.mark.parametrize("repo_type", ["public", "access-token"])
def test_no_access_token_when_public(
    repo_type: RepoType, access_token: None | str
) -> None:
    attrs = {
        "repo_type": repo_type,
        "access_token": access_token,
    }

    try:
        validators.validate_no_access_token_when_public(attrs, ProjectSerializer())
    except ValidationError:
        assert repo_type == "public"
        assert access_token


@pytest.mark.parametrize("access_token", [None, "token"])
@pytest.mark.parametrize("is_public", [True, False])
@pytest.mark.parametrize("repo_type", ["public", "access-token"])
@pytest.mark.parametrize("remote_exists", [True, False])
def test_remote_exists(  # noqa: C901
    repo_type: str,
    access_token: str | None,
    is_public: bool,
    remote_exists: bool,
    mocker: MockerFixture,
) -> None:
    def side_effect(url: str) -> bool:
        if not remote_exists:
            return False
        if repo_type == "public":
            return True
        return is_public or "@" in url

    check_remote_existance_mock = mocker.patch.object(
        validators, "check_remote_existance", side_effect=side_effect
    )

    attrs = {
        "repo": "my.git.com/foo/bar",
        "repo_type": repo_type,
    }

    if access_token:
        attrs["access_token"] = access_token

    try:
        validators.validate_remote_url(attrs, ProjectSerializer())
        if repo_type == "access-token" and access_token:
            check_remote_existance_mock.assert_has_calls(
                [call("outdated:token@my.git.com/foo/bar"), call("my.git.com/foo/bar")]
            )
            assert remote_exists
            return
        if (
            repo_type == "access-token"
            and not access_token
            or repo_type == "public"
            and access_token
        ):
            check_remote_existance_mock.assert_not_called()
            return
        check_remote_existance_mock.assert_called_once()
        assert remote_exists
    except ValidationError as e:
        if not remote_exists:
            assert e.message == "Repository does not exist."  # noqa: PT017
            return
        assert e.message == "Repository is public."  # noqa: PT017
        assert is_public
        assert access_token
        assert repo_type == "access-token"


@pytest.mark.django_db()
@pytest.mark.parametrize("repo", ["my.git.com/foo/bar", "other.git.com/foo/bar"])
@pytest.mark.parametrize("repo_type", ["public", "access-token"])
def test_remote_exists_with_instance(
    repo_type: RepoType,
    repo: str,
    mocker: MockerFixture,
    project_factory: ProjectFactory,
) -> None:
    check_remote_existance_mock = mocker.patch.object(
        validators, "check_remote_existance"
    )

    project = project_factory(repo="my.git.com/foo/bar", repo_type="public")

    attrs = {"repo": repo, "repo_type": repo_type}

    if repo_type == "access-token":
        attrs["access_token"] = "token"  # noqa: S105

    serializer = ProjectSerializer(project)

    with suppress(ValidationError):
        validators.validate_remote_url(attrs, serializer)

    if project.repo == repo and project.repo_type == repo_type:
        check_remote_existance_mock.assert_not_called()
    else:
        check_remote_existance_mock.assert_called()


@pytest.mark.parametrize(
    "exists",
    [True, False],
)
def test_check_remote_exists(exists: bool, tmp_repo_root: Path) -> None:
    path = tmp_repo_root.absolute() / "project"
    url = f"file://{path.absolute()}"
    if exists:
        path.mkdir()
        run(["/usr/bin/git", "init"], shell=False, check=False, cwd=path)
    assert validators.check_remote_existance(url) == exists
