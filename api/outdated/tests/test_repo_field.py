from __future__ import annotations

from subprocess import run
from typing import TYPE_CHECKING

import pytest
from django.core.exceptions import ValidationError

from outdated.models import validate_repo_exists

if TYPE_CHECKING:
    from pathlib import Path


@pytest.mark.parametrize(
    "exists",
    [True, False],
)
def test_repository_exists_validator(exists: bool, tmp_repo_root: Path) -> None:
    path = tmp_repo_root.absolute() / "project"
    url = f"file://{path.absolute()}"
    if exists:
        path.mkdir()
        run(["/usr/bin/git", "init"], shell=False, check=False, cwd=path)
    try:
        validate_repo_exists(url)
        assert exists
    except ValidationError:
        assert not exists
