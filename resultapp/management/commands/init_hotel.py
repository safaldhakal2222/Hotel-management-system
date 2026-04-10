from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from resultapp.models import Hotel, RoomType, Staff
from datetime import date


class Command(BaseCommand):
    help = 'Initialize hotel management system with sample data'

    def add_arguments(self, parser):
        parser.add_argument('--hotel-name', type=str, default='Main Hotel', help='Hotel name')
        parser.add_argument('--admin-username', type=str, default='admin', help='Admin username')

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting initialization...'))

        # Create Hotel
        hotel, created = Hotel.objects.get_or_create(
            name=options['hotel_name'],
            defaults={
                'address': '123 Main Street',
                'city': 'New York',
                'state': 'NY',
                'postal_code': '10001',
                'phone': '+1-800-HOTEL-1',
                'email': 'info@hotel.com',
                'total_rooms': 100,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Created hotel: {hotel.name}'))
        else:
            self.stdout.write(f'Hotel {hotel.name} already exists')

        # Create Room Types
        room_types = [
            {'name': 'Single', 'capacity': 1, 'base_price': 100},
            {'name': 'Double', 'capacity': 2, 'base_price': 150},
            {'name': 'Suite', 'capacity': 4, 'base_price': 250},
            {'name': 'Deluxe', 'capacity': 2, 'base_price': 200},
        ]

        for rt in room_types:
            room_type, created = RoomType.objects.get_or_create(
                name=rt['name'],
                defaults={
                    'capacity': rt['capacity'],
                    'base_price': rt['base_price'],
                    'description': f'{rt["name"]} room',
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created room type: {room_type.name}'))

        # Create Admin User
        admin_user, created = User.objects.get_or_create(
            username=options['admin_username'],
            defaults={
                'is_staff': True,
                'is_superuser': True,
                'email': 'admin@hotel.com',
                'first_name': 'Admin',
                'last_name': 'User',
            }
        )

        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS(f'✓ Created admin user: {admin_user.username}'))

        # Create Staff Position
        staff, created = Staff.objects.get_or_create(
            user=admin_user,
            defaults={
                'employee_id': 'EMP-001',
                'position': 'Manager',
                'department': 'Management',
                'shift': 'Morning',
                'phone': '+1-800-HOTEL-1',
                'hire_date': date.today(),
                'salary': 5000,
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Created staff: {admin_user.first_name}'))

        self.stdout.write(self.style.SUCCESS('✓ Initialization complete!'))
        self.stdout.write(self.style.SUCCESS(f'Admin username: {options["admin_username"]}, password: admin123'))
