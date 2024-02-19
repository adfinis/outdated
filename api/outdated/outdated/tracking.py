from __future__ import annotations

from pathlib import Path
from shutil import rmtree
from subprocess import run
from typing import TYPE_CHECKING

from django.conf import settings

from .parser import LockfileParser

if TYPE_CHECKING:
    from subprocess import CompletedProcess

    from outdated.outdated.models import Project


class RepoError(ValueError):
    """Raise when there is an error with the repositories."""


class Tracker:
    def __init__(self, project: Project, access_token: str | None = None) -> None:
        self.project = project
        self.access_token = access_token
        self.local_path = Path(f"{settings.REPOSITORY_ROOT}/{self.project.clone_path}")

    def _run(
        self,
        command: list[str],
        requires_local_copy: bool = False,
    ) -> CompletedProcess[str]:
        if not self.local_path.exists() and requires_local_copy:
            raise RepoError(
                f"Can't run {command} without local copy of {self.project.repo}",
            )
        return run(
            command,
            cwd=self.repository_path,
            capture_output=True,
            check=False,
        )

    def clone(self):
        self.delete()
        url = (
            "https://"
            + (f"outdated:{self.access_token}@" if self.access_token else "")
            + self.project.repo
        )
        self._run(
            [
                "git",
                "clone",
                "-n",
                "--depth=1",
                "--filter=tree:0",
                "--single-branch",
                url,
                self.local_path.absolute(),
            ],
        )
        self._run(
            [
                "git",
                "sparse-checkout",
                "set",
                "--no-cone",
                *settings.SUPPORTED_LOCK_FILES,
            ],
        )

    def checkout(self):
        return self._run(["git", "checkout"], True)

    @property
    def lockfiles(self):
        if not self.local_path.exists():
            raise RepoError(
                f"Unable to retrieve lockfiles for {self.project.repo} because it is not saved locally.",
            )

        lockfile_list = []
        for root, dirs, files in self.local_path.walk():
            if ".git" in dirs:
                dirs.remove(".git")

            lockfile_list.extend(
                [
                    Path(root).joinpath(file)
                    for file in files
                    if not Path(root).joinpath(file).is_symlink()
                ]
            )

        return lockfile_list

    @property
    def repository_path(self):
        return (
            self.local_path.absolute()
            if self.local_path.exists()
            else Path(settings.REPOSITORY_ROOT)
        )

    def sync(self):
        if not self.local_path.exists():
            self.clone()
        self.checkout()
        dependencies = LockfileParser(self.lockfiles).parse()
        self.project.versioned_dependencies.set(dependencies)

    def setup(self):  # pragma: no cover
        self.clone()
        self.checkout()
        self.sync()

    def delete(self):  # pragma: no cover
        rmtree(self.local_path, True)
        self._run(
            [
                "rmdir",
                "-p",
                "--ignore-fail-on-non-empty",
                self.local_path.parent.absolute(),
            ],
        )
