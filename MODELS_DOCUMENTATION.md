# Hotel Management System - Models Documentation

## Overview

This document provides detailed information about all models in the Hotel Management System.

---

## 🏨 Hotel Model

**Purpose:** The central model representing a hotel property.

**Fields:**
- `name` (CharField, max_length=200) - Hotel name
- `address` (TextField) - Street address
- `city` (CharField, max_length=100) - City name
- `state` (CharField, max_length=100) - State/Province
- `postal_code` (CharField, max_length=20) - Postal code
- `phone` (CharField, max_length=15) - Contact phone
- `email` (EmailField) - Contact email
- `website` (URLField, optional) - Hotel website
- `total_rooms` (IntegerField) - Total number of rooms
- `created_at` (DateTimeField, auto) - Creation timestamp
- `updated_at` (DateTimeField, auto) - Last update timestamp

**Relationships:**
- OneToMany: rooms, bookings

**Example:**
```python
hotel = Hotel.objects.create(
    name="Grand Hotel",
    address="123 Main Street",
    city="New York",
    state="NY",
    postal_code="10001",
    phone="+1-800-123-4567",
    email="info@grandhotel.com",
    website="https://grandhotel.com",
    total_rooms=200
)
```

---

## 🛏️ RoomType Model

**Purpose:** Defines different types of rooms available in the hotel.

**Fields:**
- `name` (CharField, max_length=50) - Type name (e.g., "Single", "Double")
- `description` (TextField, optional) - Type description
- `base_price` (DecimalField) - Base price per night
- `capacity` (IntegerField) - Number of people
- `amenities` (TextField, optional) - Comma-separated list of amenities

**Example:**
```python
room_type = RoomType.objects.create(
    name="Deluxe Suite",
    description="Luxury suite with king bed and city view",
    base_price=250.00,
    capacity=3,
    amenities="WiFi, TV, Air Conditioning, Mini Bar, Bathrobe"
)
```

---

## 🚪 Room Model

**Purpose:** Represents individual rooms in the hotel.

**Fields:**
- `hotel` (ForeignKey to Hotel) - Hotel this room belongs to
- `room_number` (CharField, max_length=10) - Room number
- `room_type` (ForeignKey to RoomType) - Type of room
- `floor` (IntegerField) - Floor number
- `status` (CharField, choices) - Room status
  - 'Available' - Ready for check-in
  - 'Occupied' - Currently occupied
  - 'Maintenance' - Under maintenance
  - 'Reserved' - Reserved for future booking
- `price_per_night` (DecimalField) - Nightly rate
- `is_available` (BooleanField) - Available for booking
- `description` (TextField, optional) - Room notes
- `created_at` (DateTimeField, auto)
- `updated_at` (DateTimeField, auto)

**Constraints:**
- `unique_together` - ("hotel", "room_number")

**Relationships:**
- ManyToOne: hotel, room_type
- OneToMany: bookings

**Example:**
```python
room = Room.objects.create(
    hotel=hotel,
    room_number="301",
    room_type=room_type,
    floor=3,
    status="Available",
    price_per_night=250.00,
    is_available=True,
    description="Deluxe corner room with city view"
)
```

---

## 👥 Guest Model

**Purpose:** Stores information about hotel guests.

**Fields:**
- `user` (OneToOneField to User, optional) - Django user account
- `first_name` (CharField, max_length=100)
- `last_name` (CharField, max_length=100)
- `email` (EmailField)
- `phone` (CharField, max_length=15)
- `address` (TextField, optional)
- `city` (CharField, optional)
- `country` (CharField, max_length=100, optional)
- `postal_code` (CharField, optional)
- `gender` (CharField, choices, optional)
  - 'M' - Male
  - 'F' - Female
  - 'O' - Other
- `id_type` (CharField, optional) - Type of ID (Passport, License, etc.)
- `id_number` (CharField, optional) - ID number
- `date_of_birth` (DateField, optional)
- `total_bookings` (IntegerField, default=0) - Total bookings made
- `created_at` (DateTimeField, auto)
- `updated_at` (DateTimeField, auto)

**Relationships:**
- OneToOne: user
- OneToMany: bookings

**Example:**
```python
guest = Guest.objects.create(
    first_name="John",
    last_name="Doe",
    email="john@example.com",
    phone="+1-555-0123",
    address="456 Oak Street",
    city="Boston",
    country="USA",
    gender="M",
    id_type="Passport",
    id_number="AB123456"
)
```

---

## 📅 Booking Model

**Purpose:** Manages room bookings and reservations.

**Fields:**
- `booking_id` (CharField, unique) - Auto-generated booking ID (BK-XXXXXXXX)
- `hotel` (ForeignKey to Hotel)
- `guest` (ForeignKey to Guest)
- `room` (ForeignKey to Room)
- `check_in_date` (DateField)
- `check_out_date` (DateField)
- `number_of_guests` (IntegerField) - Number of people
- `status` (CharField, choices)
  - 'Pending' - Awaiting confirmation
  - 'Confirmed' - Booking confirmed
  - 'Checked In' - Guest checked in
  - 'Checked Out' - Guest checked out
  - 'Cancelled' - Booking cancelled
- `number_of_nights` (IntegerField) - Auto-calculated
- `total_price` (DecimalField) - Total booking cost
- `notes` (TextField, optional) - Special requests
- `created_at` (DateTimeField, auto)
- `updated_at` (DateTimeField, auto)

**Relationships:**
- ManyToOne: hotel, guest, room
- OneToOne: payment
- OneToMany: services, reviews, complaints

**Auto-Calculate Behavior:**
- On save, generates unique booking_id if not present
- Calculates number_of_nights from dates

**Example:**
```python
from datetime import date, timedelta

booking = Booking.objects.create(
    hotel=hotel,
    guest=guest,
    room=room,
    check_in_date=date.today(),
    check_out_date=date.today() + timedelta(days=3),
    number_of_guests=2,
    total_price=750.00,
    notes="Late arrival expected, have limo service"
)
```

---

## 💳 Payment Model

**Purpose:** Tracks payments for bookings.

**Fields:**
- `booking` (OneToOneField to Booking) - Associated booking
- `amount` (DecimalField) - Payment amount
- `payment_method` (CharField, choices)
  - 'Credit Card'
  - 'Debit Card'
  - 'Cash'
  - 'Bank Transfer'
  - 'Online'
- `status` (CharField, choices)
  - 'Pending' - Not yet processed
  - 'Completed' - Successfully paid
  - 'Failed' - Payment failed
  - 'Refunded' - Payment refunded
- `transaction_id` (CharField, optional) - External transaction ID
- `notes` (TextField, optional)
- `paid_at` (DateTimeField, optional) - Payment timestamp
- `created_at` (DateTimeField, auto)
- `updated_at` (DateTimeField, auto)

**Example:**
```python
payment = Payment.objects.create(
    booking=booking,
    amount=750.00,
    payment_method="Credit Card",
    status="Completed",
    transaction_id="TXN-ABC123XYZ",
    paid_at=timezone.now()
)
```

---

## 👨‍💼 Staff Model

**Purpose:** Manages hotel staff information.

**Fields:**
- `user` (OneToOneField to User) - Django user account
- `employee_id` (CharField, unique, max_length=20) - Employee ID
- `position` (CharField, choices)
  - 'Manager' - Hotel manager
  - 'Receptionist' - Front desk
  - 'Housekeeper' - Room cleaning
  - 'Chef' - Kitchen staff
  - 'Waiter' - Restaurant staff
  - 'Security' - Security staff
  - 'Maintenance' - Maintenance staff
- `department` (CharField, optional) - Department name
- `shift` (CharField, choices)
  - 'Morning' (6 AM - 2 PM)
  - 'Evening' (2 PM - 10 PM)
  - 'Night' (10 PM - 6 AM)
- `phone` (CharField, max_length=15)
- `hire_date` (DateField)
- `salary` (DecimalField)
- `is_active` (BooleanField, default=True)
- `created_at` (DateTimeField, auto)
- `updated_at` (DateTimeField, auto)

**Relationships:**
- OneToOne: user
- OneToMany: maintenance_requests

**Example:**
```python
from django.contrib.auth.models import User
from datetime import date

user = User.objects.create_user(
    username="john_smith",
    email="john@hotel.com",
    first_name="John",
    last_name="Smith"
)

staff = Staff.objects.create(
    user=user,
    employee_id="EMP-001",
    position="Manager",
    department="Management",
    shift="Morning",
    phone="+1-555-0123",
    hire_date=date(2023, 1, 1),
    salary=5000.00
)
```

---

## 🛎️ Service Model

**Purpose:** Defines available hotel services and amenities.

**Fields:**
- `name` (CharField, max_length=100)
- `service_type` (CharField, choices)
  - 'Room Service'
  - 'Laundry'
  - 'Spa'
  - 'Gym'
  - 'Restaurant'
  - 'Parking'
  - 'Tours'
  - 'Other'
- `description` (TextField)
- `price` (DecimalField)
- `is_available` (BooleanField, default=True)
- `created_at` (DateTimeField, auto)

**Relationships:**
- OneToMany: booking_services

**Example:**
```python
service = Service.objects.create(
    name="Airport Transfer",
    service_type="Tours",
    description="Complimentary airport transfer",
    price=0.00,
    is_available=True
)
```

---

## 🛏️ BookingService Model

**Purpose:** Links services to bookings.

**Fields:**
- `booking` (ForeignKey to Booking)
- `service` (ForeignKey to Service)
- `quantity` (IntegerField, default=1)
- `price` (DecimalField) - Price at time of booking
- `added_on` (DateTimeField, auto)

**Example:**
```python
booking_service = BookingService.objects.create(
    booking=booking,
    service=service,
    quantity=2,
    price=40.00  # 2 × $20
)
```

---

## ⭐ Review Model

**Purpose:** Stores guest reviews and ratings.

**Fields:**
- `booking` (OneToOneField to Booking)
- `guest` (ForeignKey to Guest)
- `rating` (IntegerField, choices 1-5)
- `cleanliness` (IntegerField, choices 1-5)
- `service` (IntegerField, choices 1-5)
- `food` (IntegerField, choices 1-5)
- `comment` (TextField) - Review text
- `would_recommend` (BooleanField, default=True)
- `reviewed_at` (DateTimeField, auto)

**Example:**
```python
review = Review.objects.create(
    booking=booking,
    guest=guest,
    rating=5,
    cleanliness=5,
    service=4,
    food=4,
    comment="Excellent stay! Great service and clean rooms.",
    would_recommend=True
)
```

---

## 🔧 MaintenanceRequest Model

**Purpose:** Tracks maintenance and repair requests.

**Fields:**
- `room` (ForeignKey to Room)
- `priority` (CharField, choices)
  - 'Low' - Non-urgent
  - 'Medium' - Normal priority
  - 'High' - Urgent
  - 'Urgent' - Critical
- `description` (TextField) - Issue description
- `status` (CharField, choices)
  - 'Open' - Not started
  - 'In Progress' - Being worked on
  - 'Completed' - Finished
  - 'Cancelled' - Cancelled
- `assigned_to` (ForeignKey to Staff, optional)
- `created_at` (DateTimeField, auto)
- `completed_at` (DateTimeField, optional)

**Example:**
```python
maintenance = MaintenanceRequest.objects.create(
    room=room,
    priority="High",
    description="AC unit not working in room 301",
    status="Open",
    assigned_to=staff
)
```

---

## 📝 Complaint Model

**Purpose:** Handles guest complaints.

**Fields:**
- `booking` (ForeignKey to Booking)
- `guest` (ForeignKey to Guest)
- `complaint_type` (CharField, choices)
  - 'Cleanliness'
  - 'Noise'
  - 'Service'
  - 'Facilities'
  - 'Other'
- `description` (TextField)
- `status` (CharField, choices)
  - 'Open' - New complaint
  - 'In Progress' - Being handled
  - 'Resolved' - Handled
  - 'Closed' - Closed
- `resolution` (TextField, optional) - How it was resolved
- `created_at` (DateTimeField, auto)
- `resolved_at` (DateTimeField, optional)

**Example:**
```python
complaint = Complaint.objects.create(
    booking=booking,
    guest=guest,
    complaint_type="Noise",
    description="Neighbors were too loud late at night",
    status="Open"
)
```

---

## Relationships Summary

```
Hotel
  ├─ 1:Many → Room
  └─ 1:Many → Booking

RoomType
  └─ 1:Many → Room

Room
  ├─ Many:1 → Hotel
  ├─ Many:1 → RoomType
  └─ 1:Many → Booking
     └─ 1:Many → MaintenanceRequest

Guest
  ├─ 1:1 → User
  └─ 1:Many → Booking

Booking
  ├─ Many:1 → Hotel
  ├─ Many:1 → Guest
  ├─ Many:1 → Room
  ├─ 1:1 → Payment
  ├─ 1:Many → BookingService
  ├─ 1:1 → Review
  └─ 1:Many → Complaint

Service
  └─ 1:Many → BookingService

BookingService
  ├─ Many:1 → Booking
  └─ Many:1 → Service

Staff
  ├─ 1:1 → User
  └─ 1:Many → MaintenanceRequest
```

---

## Usage Examples

### Query All Bookings for a Guest
```python
guest = Guest.objects.get(id=1)
bookings = guest.bookings.all()
```

### Get Reviews for a Hotel
```python
hotel = Hotel.objects.get(id=1)
reviews = Review.objects.filter(booking__hotel=hotel)
avg_rating = reviews.aggregate(Avg('rating'))
```

### Get Occupied Rooms
```python
occupied_rooms = Room.objects.filter(status='Occupied')
```

### Get Pending Payments
```python
pending_payments = Payment.objects.filter(status='Pending')
```

### Get Staff by Position
```python
managers = Staff.objects.filter(position='Manager', is_active=True)
```

### Get Maintenance Requests
```python
open_requests = MaintenanceRequest.objects.filter(status='Open').order_by('priority')
```

---

For more information, refer to the main README.md and API_DOCUMENTATION.md files.
