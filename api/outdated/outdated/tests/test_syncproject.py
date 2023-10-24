from unittest.mock import ANY

import pytest
from django.core.management import call_command

from outdated.outdated.synchroniser import Synchroniser


@pytest.mark.vcr()
@pytest.mark.django_db(transaction=True)
def test_syncproject(project_factory, mocker):
    project = project_factory.create(repo="https://github.com/projectcaluma/caluma")
    sync_init_mocker = mocker.spy(Synchroniser, "__init__")
    call_command("syncproject", project.name)
    sync_init_mocker.assert_called_once_with(ANY, project)
