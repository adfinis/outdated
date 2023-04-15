from django.core.management.base import BaseCommand

from asyncio import run


class AsyncCommand(BaseCommand):
    def handle(self, *args, **options):
        run(self._handle(*args, **options))
