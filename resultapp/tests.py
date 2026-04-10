from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from datetime import date, timedelta
from .models import Hotel, RoomType, Room, Guest, Booking, Payment, Staff


class HotelModelTest(TestCase):
    """Test Hotel Model"""
    
    def setUp(self):
        self.hotel = Hotel.objects.create(
            name="Test Hotel",
            address="123 Main St",
            city="Test City",
            state="Test State",
            postal_code="12345",
            phone="555-1234",
            email="hotel@test.com",
            total_rooms=10
        )
    
    def test_hotel_creation(self):
        self.assertEqual(self.hotel.name, "Test Hotel")
        self.assertEqual(self.hotel.city, "Test City")
        self.assertTrue(Hotel.objects.filter(name="Test Hotel").exists())


class RoomModelTest(TestCase):
    """Test Room Model"""
    
    def setUp(self):
        self.hotel = Hotel.objects.create(
            name="Test Hotel",
            address="123 Main St",
            city="Test City",
            state="Test State",
            postal_code="12345",
            phone="555-1234",
            email="hotel@test.com",
            total_rooms=10
        )
        
        self.room_type = RoomType.objects.create(
            name="Single",
            base_price=50.00,
            capacity=1
        )
        
        self.room = Room.objects.create(
            hotel=self.hotel,
            room_number="101",
            room_type=self.room_type,
            floor=1,
            price_per_night=50.00,
            is_available=True
        )
    
    def test_room_creation(self):
        self.assertEqual(self.room.room_number, "101")
        self.assertTrue(self.room.is_available)
        self.assertEqual(self.room.status, "Available")


class BookingModelTest(TestCase):
    """Test Booking Model"""
    
    def setUp(self):
        self.hotel = Hotel.objects.create(
            name="Test Hotel",
            address="123 Main St",
            city="Test City",
            state="Test State",
            postal_code="12345",
            phone="555-1234",
            email="hotel@test.com",
            total_rooms=10
        )
        
        self.room_type = RoomType.objects.create(
            name="Single",
            base_price=50.00,
            capacity=1
        )
        
        self.room = Room.objects.create(
            hotel=self.hotel,
            room_number="101",
            room_type=self.room_type,
            floor=1,
            price_per_night=100.00,
            is_available=True
        )
        
        self.guest = Guest.objects.create(
            first_name="John",
            last_name="Doe",
            email="john@test.com",
            phone="555-1234"
        )
        
        self.check_in = date.today()
        self.check_out = self.check_in + timedelta(days=3)
        
        self.booking = Booking.objects.create(
            hotel=self.hotel,
            guest=self.guest,
            room=self.room,
            check_in_date=self.check_in,
            check_out_date=self.check_out,
            number_of_guests=1,
            number_of_nights=3,
            total_price=300.00
        )
    
    def test_booking_creation(self):
        self.assertEqual(self.booking.guest.first_name, "John")
        self.assertEqual(self.booking.status, "Pending")
        self.assertTrue(self.booking.booking_id.startswith("BK-"))
    
    def test_booking_nights_calculation(self):
        self.assertEqual(self.booking.number_of_nights, 3)


class StaffModelTest(TestCase):
    """Test Staff Model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username="staff1",
            password="testpass123",
            first_name="John",
            last_name="Staff"
        )
        
        self.staff = Staff.objects.create(
            user=self.user,
            employee_id="EMP001",
            position="Manager",
            shift="Morning",
            phone="555-1234",
            hire_date=date.today(),
            salary=50000.00
        )
    
    def test_staff_creation(self):
        self.assertEqual(self.staff.employee_id, "EMP001")
        self.assertEqual(self.staff.position, "Manager")
        self.assertTrue(self.staff.is_active)


class APITestCase(TestCase):
    """API endpoint tests"""
    
    def setUp(self):
        self.hotel = Hotel.objects.create(
            name="Test Hotel",
            address="123 Main St",
            city="Test City",
            state="Test State",
            postal_code="12345",
            phone="555-1234",
            email="hotel@test.com",
            total_rooms=10
        )
    
    def test_hotel_api(self):
        """Test hotel API endpoint"""
        response = self.client.get('/api/hotels/')
        self.assertEqual(response.status_code, 200)

