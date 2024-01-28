# yourapp/management/commands/import_shops_json.py
import json
from django.core.management.base import BaseCommand
from gate_time.models import Gate

class Command(BaseCommand):
    help = 'Import shop data from JSON file'

    def handle(self, *args, **options):
        with open('gates.json') as json_file:
            data = json.load(json_file)
        
        for shop_data in data["gate"]:
            Gate.objects.create(
                name=shop_data['name'],
                latitude=float(shop_data['latitude']),
                longitude=float(shop_data['longitude'])
            )

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
