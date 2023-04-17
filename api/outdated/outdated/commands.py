from asyncio import run

from django.core.management.base import BaseCommand


class AsyncCommand(BaseCommand):
    def handle(self, *args, **options):
        run(self._handle(*args, **options))
