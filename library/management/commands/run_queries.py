from django.core.management.base import BaseCommand

from library.queries import run_all


class Command(BaseCommand):
    help = "Выполняет все запросы из library/queries.py и печатает результаты"

    def handle(self, *args, **options):
        run_all(out=self.stdout.write)
