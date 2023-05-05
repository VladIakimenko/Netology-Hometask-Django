import csv
import decimal
from datetime import datetime

from django.core.management.base import BaseCommand
from phones.models import Phone


class Command(BaseCommand):
    help = 'Imports dump from a csv.'

    def add_arguments(self, parser):
        parser.add_argument(
            '-f',
            '--file',
            help='Path to the CSV dump to import to DB. '
                 'Can use relative path from BASE_DIR.',
            required=True,
        )

    def handle(self, *args, **options):
        file_path = options['file']
        with open(file_path, 'r') as file:
            phones = list(csv.DictReader(file, delimiter=';'))

        for phone in phones:
            Phone.objects.create(
                name=phone['name'],
                price=decimal.Decimal(phone['price']),
                image=phone['image'],
                release_date=datetime.strptime(phone['release_date'], '%Y-%m-%d').date(),
                lte_exists=bool(phone['lte_exists']),
            )
