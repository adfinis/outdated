from __future__ import annotations

from pathlib import Path
from subprocess import run
from typing import TYPE_CHECKING

from django.conf import settings

from outdated.parser import LockFileParser

if TYPE_CHECKING:
    from subprocess import CompletedProcess

    from outdated.outdated.models import Project


class RepoError(ValueError):
    """Raise when there is an error with the repositories."""


class Tracker:
    def __init__(self, project: Project) -> None:
        self.project = project
        self.local_path = Path(f"/projects/{self.project.clone_path}")

    def _run(
        self,
        command: list[str],
        fail_without_local_copy: bool = False,  # noqa: FBT001,FBT002
    ) -> CompletedProcess[str]:
        if not self.has_local_copy and fail_without_local_copy:
            msg = f"Can't run {command} without local copy of {self.project.repo}"
            raise RepoError(msg)
        return run(
            command,  # noqa: S603
            cwd=self.repository_path,
            capture_output=True,
            check=False,
        )

    def clone(self):  # pragma: no cover
        self.delete()
        self._run(
            [
                "git",
                "clone",
                "-n",
                "--depth=1",
                "--filter=tree:0",
                "--single-branch",
                "https://" + self.project.repo,
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

    def checkout(self):  # pragma: no cover
        return self._run(["git", "checkout"], fail_without_local_copy=True)

    @property
    def lockfiles(self):
        if not self.has_local_copy:
            msg = f"Unable to retrieve lockfiles for {self.project.repo} because it is not saved locally."
            raise RepoError(msg)

        lockfile_list = []
        for root, dirs, files in self.local_path.walk():
            if ".git" in dirs:
                dirs.remove(".git")

            lockfile_list.extend([Path(root).joinpath(file) for file in files])

        return lockfile_list

    @property
    def has_local_copy(self):  # pragma: no cover
        return self.local_path.exists()

    @property
    def repository_path(self):
        return self.local_path.absolute() if self.has_local_copy else "/projects/"

    def sync(self):
        if not self.has_local_copy:
            self.clone()
        self.checkout()
        dependencies = LockFileParser(self.lockfiles).parse()
        self.project.versioned_dependencies.set(dependencies)

    def setup(self):  # pragma: no cover
        self.clone()
        self.checkout()
        self.sync()

    def delete(self):  # pragma: no cover
        self._run(["rm", "-rf", self.local_path])
        self._run(
            [
                "rmdir",
                "-p",
                "--ignore-fail-on-non-empty",
                "basename",
                f"/projects/{self.project.repo_domain}/{self.project.repo_namespace}",
            ],
        )
