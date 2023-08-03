from django.core.mail import EmailMessage
from django.template.base import Template
from django.template.loader import get_template

from outdated.outdated.models import Project

from .models import Notification


class Notifier:
    def __init__(self, project: Project) -> None:
        self.project = project

    def notify(self) -> None:
        try:
            notification: Notification = self.project.notification_queue.get(
                schedule__gte=self.project.duration_until_outdated
            )
        except Notification.DoesNotExist:
            return

        template: Template = get_template(notification.template + ".txt", using="text")
        subject, _, body = template.render({"project": self.project}).partition("\n")
        maintainers = [m.user.email for m in self.project.maintainers.all()]
        message = EmailMessage(subject, body, to=maintainers[:1], cc=maintainers[1:])
        message.send()
        self.project.notification_queue.remove(notification)
        self.project.save()
