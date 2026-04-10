from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from datetime import timedelta

# ============ HOTEL INFORMATION ============

class Hotel(models.Model):
    """Main hotel information"""
    name = models.CharField(max_length=200)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    website = models.URLField(blank=True, null=True)
    total_rooms = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Hotels"

    def __str__(self):
        return self.name


# ============ ROOM MANAGEMENT ============

class RoomType(models.Model):
    """Different types of rooms available"""
    name = models.CharField(max_length=50)  # Single, Double, Suite, etc.
    description = models.TextField(blank=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.IntegerField(validators=[MinValueValidator(1)])
    amenities = models.TextField(blank=True)  # Comma-separated list

    def __str__(self):
        return self.name


class Room(models.Model):
    """Individual rooms in the hotel"""
    ROOM_STATUS = (
        ('Available', 'Available'),
        ('Occupied', 'Occupied'),
        ('Maintenance', 'Maintenance'),
        ('Reserved', 'Reserved'),
    )

    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.CharField(max_length=10)
    room_type = models.ForeignKey(RoomType, on_delete=models.SET_NULL, null=True)
    floor = models.IntegerField()
    status = models.CharField(max_length=20, choices=ROOM_STATUS, default='Available')
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('hotel', 'room_number')
        ordering = ['floor', 'room_number']

    def __str__(self):
        return f"Room {self.room_number} - {self.room_type}"


# ============ CUSTOMER MANAGEMENT ============

class Guest(models.Model):
    """Hotel guest information"""
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    id_type = models.CharField(max_length=50, blank=True)  # Passport, License, etc.
    id_number = models.CharField(max_length=50, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    total_bookings = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# ============ BOOKING MANAGEMENT ============

class Booking(models.Model):
    """Room booking records"""
    BOOKING_STATUS = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Checked In', 'Checked In'),
        ('Checked Out', 'Checked Out'),
        ('Cancelled', 'Cancelled'),
    )

    booking_id = models.CharField(max_length=20, unique=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='bookings')
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name='bookings')
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    number_of_guests = models.IntegerField(validators=[MinValueValidator(1)])
    status = models.CharField(max_length=20, choices=BOOKING_STATUS, default='Pending')
    number_of_nights = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Booking {self.booking_id} - {self.guest}"

    def save(self, *args, **kwargs):
        if not self.booking_id:
            import uuid
            self.booking_id = f"BK-{uuid.uuid4().hex[:8].upper()}"
        if not self.number_of_nights:
            self.number_of_nights = (self.check_out_date - self.check_in_date).days
        super().save(*args, **kwargs)


# ============ PAYMENT MANAGEMENT ============

class Payment(models.Model):
    """Payment records for bookings"""
    PAYMENT_METHOD = (
        ('Credit Card', 'Credit Card'),
        ('Debit Card', 'Debit Card'),
        ('Cash', 'Cash'),
        ('Bank Transfer', 'Bank Transfer'),
        ('Online', 'Online'),
    )

    PAYMENT_STATUS = (
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
        ('Refunded', 'Refunded'),
    )

    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='Pending')
    transaction_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    notes = models.TextField(blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment {self.booking.booking_id} - {self.status}"


# ============ STAFF MANAGEMENT ============

class Staff(models.Model):
    """Hotel staff information"""
    POSITION_CHOICES = (
        ('Manager', 'Manager'),
        ('Receptionist', 'Receptionist'),
        ('Housekeeper', 'Housekeeper'),
        ('Chef', 'Chef'),
        ('Waiter', 'Waiter'),
        ('Security', 'Security'),
        ('Maintenance', 'Maintenance'),
    )

    SHIFT_CHOICES = (
        ('Morning', 'Morning (6 AM - 2 PM)'),
        ('Evening', 'Evening (2 PM - 10 PM)'),
        ('Night', 'Night (10 PM - 6 AM)'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20, unique=True)
    position = models.CharField(max_length=50, choices=POSITION_CHOICES)
    department = models.CharField(max_length=100, blank=True)
    shift = models.CharField(max_length=20, choices=SHIFT_CHOICES)
    phone = models.CharField(max_length=15)
    hire_date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} - {self.position}"


# ============ SERVICE & AMENITIES ============

class Service(models.Model):
    """Additional hotel services"""
    SERVICE_TYPE = (
        ('Room Service', 'Room Service'),
        ('Laundry', 'Laundry'),
        ('Spa', 'Spa'),
        ('Gym', 'Gym'),
        ('Restaurant', 'Restaurant'),
        ('Parking', 'Parking'),
        ('Tours', 'Tours'),
        ('Other', 'Other'),
    )

    name = models.CharField(max_length=100)
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPE)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class BookingService(models.Model):
    """Services booked by guests during their stay"""
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='services')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=10, decimal_places=2)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.booking.booking_id} - {self.service.name}"


# ============ REVIEWS & RATINGS ============

class Review(models.Model):
    """Guest reviews and ratings"""
    RATING_CHOICES = [
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent'),
    ]

    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='review')
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    cleanliness = models.IntegerField(choices=RATING_CHOICES)
    service = models.IntegerField(choices=RATING_CHOICES)
    food = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    would_recommend = models.BooleanField(default=True)
    reviewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.guest} - Rating {self.rating}"


# ============ COMPLAINTS & MAINTENANCE ============

class MaintenanceRequest(models.Model):
    """Maintenance and repair requests"""
    STATUS_CHOICES = (
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )

    PRIORITY_CHOICES = (
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Urgent', 'Urgent'),
    )

    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')
    assigned_to = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Maintenance - {self.room} - {self.priority}"


class Complaint(models.Model):
    """Guest complaints"""
    COMPLAINT_TYPE = (
        ('Cleanliness', 'Cleanliness'),
        ('Noise', 'Noise'),
        ('Service', 'Service'),
        ('Facilities', 'Facilities'),
        ('Other', 'Other'),
    )

    STATUS_CHOICES = (
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Closed', 'Closed'),
    )

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    complaint_type = models.CharField(max_length=20, choices=COMPLAINT_TYPE)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')
    resolution = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Complaint - {self.booking.booking_id}"