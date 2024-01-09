from __future__ import annotations

from subprocess import run
from typing import TYPE_CHECKING

from django.conf import settings
from django.core.exceptions import ValidationError

from outdated.validators import with_context

if TYPE_CHECKING:
    from typing import Any

    from outdated.outdated.serializers import ProjectSerializer


def check_remote_existence(url: str) -> bool:
    """Validate the existence of a remote git repository."""
    remote_url = (
        "" if url.startswith("file://") and settings.ENV == "test" else "https://"
    ) + url

    result = run(
        ["/usr/bin/git", "ls-remote", remote_url],
        capture_output=True,
        check=False,
        shell=False,
    )

    return not result.returncode


@with_context
def validate_access_token_required(
    attrs: dict[str, Any], serializer: ProjectSerializer
) -> None:
    if (
        serializer.instance
        and serializer.instance.repo_type == "access-token"
        or attrs["repo_type"] == "public"
    ):
        return
    if not attrs.get("access_token"):
        raise ValidationError("Access Token is required.", "required")


@with_context
def validate_no_access_token_when_public(
    attrs: dict[str, Any], serializer: ProjectSerializer
) -> None:
    if attrs["repo_type"] == "access-token":
        return
    if attrs.get("access_token"):
        raise ValidationError(
            "Access Token is not valid for public repositories.",
            params={"value": attrs.get("access_token")},
        )


@with_context
def validate_remote_url(attrs: dict[str, Any], serializer: ProjectSerializer) -> None:  # noqa: C901
    if (
        not settings.VALIDATE_REMOTES
        or (instance := serializer.instance)
        and instance.repo == attrs["repo"]
        and instance.repo_type == attrs["repo_type"]
    ):
        return
    url = attrs["repo"]
    if attrs["repo_type"] == "access-token":
        # other validator will handle this
        if not (access_token := attrs.get("access_token")):
            return
        url = f"outdated:{access_token}@" + url
    # other validator will handle this
    elif attrs.get("access_token"):
        return

    if not check_remote_existence(url):
        raise ValidationError("Repository does not exist.", params={"value": url})

    if attrs["repo_type"] == "access-token" and check_remote_existence(attrs["repo"]):
        raise ValidationError("Repository is public.", params={"value": url})
