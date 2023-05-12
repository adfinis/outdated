from asyncio import run

from django.core.management.base import BaseCommand


class AsyncCommand(BaseCommand):
    """Base command to run async code."""

    def handle(self, *args, **options):
        run(self._handle(*args, **options))
