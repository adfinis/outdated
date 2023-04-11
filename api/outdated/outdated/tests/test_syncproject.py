from django.core.management import call_command

from re import compile

from json import loads

from outdated.outdated.models import Project


def test_syncproject(db, project_factory, requests_mock, get_sample):
    project: Project = project_factory.create(
        name="Outdated", repo="https://github.com/adfinis/outdated"
    )

    call_command("syncproject", "project-does-not-exist")

    assert project.dependency_versions.count() == 0

    yarn_lock_url = (
        "https://api.github.com/repositories/560760559/contents/frontend/yarn.lock"
    )

    requests_mock.get(
        compile(r"https:\/\/api\.github\.com\/search\/code.*"),
        json={"items": [{"url": yarn_lock_url}]},
    )

    yarn_lock_download_url = "https://raw.githubusercontent.com/adfinis/Outdated/f4dafa49a0c0357214647e7cd79dcd0aad811a91/frontend/yarn.lock"

    requests_mock.get(
        yarn_lock_url,
        json={
            "download_url": yarn_lock_download_url,
        },
    )

    requests_mock.get(
        yarn_lock_download_url,
        text=get_sample("lockfiles/yarn"),
    )

    requests_mock.get(
        "https://registry.npmjs.org/ember-cli",
        json=loads(get_sample("release-dates/yarn.json"))["response"],
    )

    call_command("syncproject", project.name)

    assert project.dependency_versions.all().count() == 1
