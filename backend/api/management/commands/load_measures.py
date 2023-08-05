import json
import os

from api.models import MeasurementUnit
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError

DATA_ROOT = os.path.join(settings.BASE_DIR, 'data')


class Command(BaseCommand):
    help = 'loading measurement units from data in json'

    def add_arguments(self, parser):
        parser.add_argument('filename', default='measures.json', nargs='?',
                            type=str)

    def handle(self, *args, **options):
        try:
            with open(os.path.join(DATA_ROOT, options['filename']), 'r',
                      encoding='utf-8') as f:
                data = json.load(f)
                for unit in data:
                    try:
                        MeasurementUnit.objects.create(name=unit["name"])
                    except IntegrityError:
                        print(f'Мера {unit["name"]} уже есть в базе')

        except FileNotFoundError:
            raise CommandError('Файл отсутствует в директории data')
