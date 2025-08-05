from django.core.management.base import BaseCommand
from moneyfx.cron import save_actual_exchange_rates_from_ecb

class Command(BaseCommand):
    help = 'Import current ECB exchange rates into the database.'

    def handle(self, *args, **options):
        save_actual_exchange_rates_from_ecb()
        self.stdout.write(self.style.SUCCESS('ECB exchange rates imported successfully.'))
