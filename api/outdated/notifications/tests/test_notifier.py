from datetime import date, timedelta
from typing import Optional

import pytest

from outdated.notifications.notifier import Notifier
from outdated.outdated.models import Maintainer


@pytest.mark.parametrize("nonprimary_maintainers", [False, True])
@pytest.mark.parametrize(
    "days_until_outdated,template,sent",
    [
        (200, None, False),
        (60, "test-foo", True),
        (50, "test-foo", True),
        (10, "test-bar", True),
        (-20, "test-baz", True),
    ],
)
def test_send_notification(
    setup_notifications,
    days_until_outdated: int,
    template: Optional[str],
    sent: bool,
    nonprimary_maintainers: bool,
    maintainer,
    maintainer_factory,
    mailoutbox,
    version_factory,
    release_version_factory,
):
    project = maintainer.project
    release_version = release_version_factory(
        end_of_life=date.today() + timedelta(days=days_until_outdated)
    )
    version = version_factory(release_version=release_version)
    project.versioned_dependencies.add(version)
    project.save()
    if nonprimary_maintainers:
        maintainer_factory(project=project)
        maintainer_factory(project=project)
        maintainer_factory(project=project)
    nonprimary_maintainers = list(Maintainer.objects.filter(is_primary=False))
    notification_queue = list(project.notification_queue.all())
    Notifier(project).notify()
    if sent:
        mail = mailoutbox[0]
        assert mail.subject == template.replace("test-", "")
        assert (
            mail.body
            == f"Project: {project.name}\nRepo: {project.repo}\n\n{template}.txt contents\n"
        )
        assert mail.to[0] == maintainer.user.email
        assert mail.cc == [m.user.email for m in nonprimary_maintainers]
        assert notification_queue[1:] == list(project.notification_queue.all())
    else:
        assert not mailoutbox
