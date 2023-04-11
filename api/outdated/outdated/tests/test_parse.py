from json import dumps, loads

import pytest

from outdated.outdated.models import Dependency, DependencyVersion
from outdated.outdated.parse import parse

SAMPLE_PATH = "outdated/outdated/tests/samples/"


@pytest.mark.parametrize(
    "lockfile,manager",
    [
        (
            "https://raw.githubusercontent.com/adfinis/Outdated/f4dafa49a0c0357214647e7cd79dcd0aad811a91/frontend/yarn.lock",
            "yarn",
        ),
        (
            "https://raw.githubusercontent.com/adfinis/timed-frontend/3e5ce3916446bec8b3d0a1e43d4d49796bfc2190/pnpm-lock.yaml",
            "pnpm",
        ),
        (
            "https://raw.githubusercontent.com/adfinis/Outdated/f4dafa49a0c0357214647e7cd79dcd0aad811a91/api/poetry.lock",
            "poetry",
        ),
    ],
)
def test_lock_files(requests_mock, db, lockfile, manager):
    release_date_file = loads(
        open(SAMPLE_PATH + f"release-dates/{manager}.json").read()
    )

    requests_mock.get(
        lockfile,
        text=open(SAMPLE_PATH + f"lockfiles/{manager}").read(),
    )

    requests_mock.get(
        release_date_file["url"],
        text=dumps(release_date_file["response"]),
    )
    assert (
        parse(lockfile, whitelisted=["ember-cli"])
        == [
            DependencyVersion.objects.get_or_create(
                dependency=Dependency.objects.get_or_create(name="ember-cli")[0],
                version="4.11.0",
                release_date="2022-02-09",
            )[0]
        ]
        == parse(
            lockfile,
            blacklisted=["@adfinis-sygroup/eslint-config"],
        )
    )
