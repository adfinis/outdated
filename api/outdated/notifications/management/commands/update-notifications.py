from datetime import timedelta

from django.conf import settings
from django.core.management.base import BaseCommand

from outdated.notifications.models import Notification


class Command(BaseCommand):
    help = "Update notifications to match those in settings.py"

    def handle(self, *args, **options):
        notifications = []
        for template, schedule in settings.NOTIFICATIONS:
            notifications.append(
                Notification.objects.get_or_create(
                    template=template, schedule=timedelta(days=schedule)
                )[0]
            )
        [n.delete() for n in Notification.objects.all() if n not in notifications]
