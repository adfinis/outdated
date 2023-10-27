import pytest
from django.core.exceptions import ValidationError

from outdated.models import validate_repo_exists


@pytest.mark.parametrize(
    "repo,exists",
    [("github.com/adfinis/outdated", True), ("adfinis.com/adfinis/outdated", False)],
)
def test_repository_exists_validator(repo: str, exists: bool):
    try:
        validate_repo_exists(repo)
        assert exists
    except ValidationError:
        assert not exists
