# yourapp/management/commands/import_shops.py
import json
from django.core.management.base import BaseCommand
from misc_time.models import Shop, Tag

class Command(BaseCommand):
    help = 'Import shops data from JSON file'

    def handle(self, *args, **options):
        with open('airport_shops.json') as json_file:
            data = json.load(json_file)

        for shop_data in data['shops']:
            tags_data = shop_data.pop('Tags', [])
            tags = [Tag.objects.get_or_create(name=tag)[0] for tag in tags_data]

            Shop.objects.create(
                name=shop_data['name'],
                latitude=float(shop_data['latitude']),
                longitude=float(shop_data['longitude']),
                shop_type=shop_data['Type'],
            ).tags.set(tags)

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
