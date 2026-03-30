from django.core.management.base import BaseCommand
from application.models import Location, Cart, CartLocationHistory


class Command(BaseCommand):
    help = 'Seeds the database with dummy cart and location data'

    def handle(self, *args, **kwargs):

        # Clear existing data
        CartLocationHistory.objects.all().delete()
        Cart.objects.all().delete()
        Location.objects.all().delete()

        # Create locations
        locations_data = [
            ('SPD',              'RFID-001'),
            ('Operating Room 1', 'RFID-002'),
            ('Operating Room 2', 'RFID-003'),
            ('ICU',              'RFID-004'),
            ('ER',               'RFID-005'),
            ('Storage',          'RFID-006'),
        ]

        locations = []
        for name, rfid in locations_data:
            loc = Location.objects.create(name=name, rfid_reader_id=rfid)
            locations.append(loc)
            self.stdout.write(f'  Created location: {name}')

        # Create carts
        carts_data = [
            ('Cart A1', 'TAG-001', 'available',   locations[0]),
            ('Cart A2', 'TAG-002', 'in_use',      locations[1]),
            ('Cart A3', 'TAG-003', 'in_use',      locations[2]),
            ('Cart B1', 'TAG-004', 'available',   locations[3]),
            ('Cart B2', 'TAG-005', 'maintenance', locations[5]),
            ('Cart B3', 'TAG-006', 'available',   locations[0]),
            ('Cart C1', 'TAG-007', 'in_use',      locations[4]),
            ('Cart C2', 'TAG-008', 'maintenance', locations[5]),
        ]

        carts = []
        for name, tag, status, location in carts_data:
            cart = Cart.objects.create(
                name=name,
                rfid_tag=tag,
                status=status,
                current_location=location,
            )
            carts.append(cart)
            self.stdout.write(f'  Created cart: {name} ({status}) @ {location.name}')

        self.stdout.write(self.style.SUCCESS(
            f'\nDone! Created {len(locations)} locations and {len(carts)} carts.'
        ))
