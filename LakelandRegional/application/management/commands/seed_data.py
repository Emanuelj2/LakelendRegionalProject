from django.core.management.base import BaseCommand
from application.models import Location, Cart, CartLocationHistory
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Seeds the database with dummy cart and location data'

    def handle(self, *args, **kwargs):

        # Gets the current time for seeding
        now = timezone.now()

        # Clear existing data
        CartLocationHistory.objects.all().delete()
        Cart.objects.all().delete()
        Location.objects.all().delete()

        # Create locations
        locations_data = [
            ('hallway1',       'RFID-001'),
            ('hallway2',       'RFID-002'),
            ('hallway3',       'RFID-003'),
            ('washroom',       'RFID-004'),
            ('washhall',       'RFID-005'),
            ('cleanroom',      'RFID-006'),
            ('storageroom',    'RFID-007'),
        ]

        locations = []
        for name, rfid in locations_data:
            loc = Location.objects.create(name=name, rfid_reader_id=rfid)
            locations.append(loc)
            self.stdout.write(f'  Created location: {name}')

        # Create carts
        carts_data = [
            ('Cart A1', 'TAG-001', 'available',   locations[0], now - timedelta(minutes=10)),
            ('Cart A2', 'TAG-002', 'in_use',      locations[1], now - timedelta(minutes=10)),
            ('Cart A3', 'TAG-003', 'in_use',      locations[2], now - timedelta(minutes=20)),
            ('Cart B1', 'TAG-004', 'available',   locations[3], now - timedelta(minutes=30)),
            ('Cart B2', 'TAG-005', 'maintenance', locations[5], now - timedelta(minutes=50)),
            ('Cart B3', 'TAG-006', 'available',   locations[0], now - timedelta(hours=1)),
            ('Cart C1', 'TAG-007', 'in_use',      locations[4], now - timedelta(hours=2)),
            ('Cart C2', 'TAG-008', 'maintenance', locations[6], now - timedelta(hours=2)),
        ]

        carts = []
        for name, tag, status, location, last_seen in carts_data:
            cart = Cart.objects.create(
                name=name,
                rfid_tag=tag,
                status=status,
                current_location=location,
                last_seen=last_seen
            )
            carts.append(cart)
            self.stdout.write(f'  Created cart: {name} ({status}) @ {location.name}')

        self.stdout.write(self.style.SUCCESS(
            f'\nDone! Created {len(locations)} locations and {len(carts)} carts.'
        ))