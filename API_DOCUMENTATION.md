# Hotel Management System - API Documentation

## Base URL
```
http://localhost:8000/api/
```

## Authentication
The API uses session-based authentication. Include your session cookie with requests or use token authentication.

## Response Format
All responses are in JSON format.

---

## Hotel Endpoints

### List Hotels
```
GET /api/hotels/
```

**Query Parameters:**
- `search` - Search by name, city, or email
- `ordering` - Order by created_at or name
- `page` - Page number for pagination

**Response:**
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Main Hotel",
      "address": "123 Main Street",
      "city": "New York",
      "state": "NY",
      "postal_code": "10001",
      "phone": "+1-800-HOTEL-1",
      "email": "info@hotel.com",
      "website": null,
      "total_rooms": 100,
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

### Create Hotel
```
POST /api/hotels/
Content-Type: application/json

{
  "name": "New Hotel",
  "address": "456 Second Ave",
  "city": "Boston",
  "state": "MA",
  "postal_code": "02101",
  "phone": "+1-800-HOTEL-2",
  "email": "info@newhotel.com",
  "website": "https://newhotel.com",
  "total_rooms": 50
}
```

### Get Hotel Statistics
```
GET /api/hotels/{id}/statistics/
```

**Response:**
```json
{
  "total_rooms": 100,
  "available_rooms": 45,
  "total_bookings": 200,
  "total_revenue": 50000.00
}
```

---

## Room Endpoints

### List Available Rooms
```
GET /api/rooms/available/?check_in=2024-01-15&check_out=2024-01-18
```

**Query Parameters:**
- `check_in` - Check-in date (YYYY-MM-DD)
- `check_out` - Check-out date (YYYY-MM-DD)

**Response:**
```json
[
  {
    "id": 1,
    "room_number": "101",
    "room_type": 1,
    "room_type_name": "Single",
    "floor": 1,
    "status": "Available",
    "price_per_night": 100.00,
    "is_available": true
  }
]
```

### Get All Rooms
```
GET /api/rooms/
```

**Query Parameters:**
- `search` - Search by room_number, room_type, or status
- `ordering` - Order by room_number, price_per_night, or floor
- `page` - Page number

### Create Room
```
POST /api/rooms/
Content-Type: application/json

{
  "hotel": 1,
  "room_number": "101",
  "room_type": 1,
  "floor": 1,
  "status": "Available",
  "price_per_night": 100.00,
  "is_available": true,
  "description": "Comfortable single room"
}
```

### Mark Room for Maintenance
```
POST /api/rooms/{id}/mark_maintenance/
```

---

## Booking Endpoints

### Create Booking
```
POST /api/bookings/
Content-Type: application/json

{
  "hotel": 1,
  "guest": 1,
  "room": 1,
  "check_in_date": "2024-01-15",
  "check_out_date": "2024-01-18",
  "number_of_guests": 2,
  "notes": "Late arrival"
}
```

**Response:** Creates booking with booking_id and automatic payment record
```json
{
  "id": 1,
  "booking_id": "BK-A1B2C3D4",
  "hotel": 1,
  "guest": {...},
  "room": {...},
  "check_in_date": "2024-01-15",
  "check_out_date": "2024-01-18",
  "number_of_guests": 2,
  "status": "Pending",
  "number_of_nights": 3,
  "total_price": 300.00,
  "notes": "Late arrival",
  "payment": {...},
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### List Bookings
```
GET /api/bookings/
```

**Query Parameters:**
- `search` - Search by booking_id or guest name
- `ordering` - Order by check_in_date, total_price, or created_at
- `status` - Filter by status

### Get Upcoming Bookings
```
GET /api/bookings/upcoming/
```

### Confirm Booking
```
POST /api/bookings/{id}/confirm/
```

### Check In Guest
```
POST /api/bookings/{id}/check_in/
```

### Check Out Guest
```
POST /api/bookings/{id}/check_out/
```

### Cancel Booking
```
POST /api/bookings/{id}/cancel/
```

---

## Payment Endpoints

### Create Payment
```
POST /api/payments/
Content-Type: application/json

{
  "booking": 1,
  "amount": 300.00,
  "payment_method": "Credit Card",
  "status": "Pending",
  "transaction_id": "TXN-ABC123",
  "notes": "Payment for booking"
}
```

### Process Payment
```
POST /api/payments/{id}/process_payment/
```

**Response:**
```json
{
  "status": "Payment processed",
  "booking_status": "Confirmed"
}
```

### List Payments
```
GET /api/payments/
```

**Query Parameters:**
- `search` - Search by booking_id or transaction_id
- `status` - Filter by status

---

## Guest Endpoints

### Create Guest
```
POST /api/guests/
Content-Type: application/json

{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "phone": "+1-555-0123",
  "address": "123 Main St",
  "city": "New York",
  "country": "USA",
  "postal_code": "10001",
  "gender": "M",
  "id_type": "Passport",
  "id_number": "AB123456",
  "date_of_birth": "1990-01-01"
}
```

### List Guests
```
GET /api/guests/
```

**Query Parameters:**
- `search` - Search by name, email, or phone
- `ordering` - Order by name, total_bookings, or created_at

### Get Guest Bookings
```
GET /api/guests/{id}/bookings/
```

---

## Service Endpoints

### List Services
```
GET /api/services/
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Room Service",
    "service_type": "Room Service",
    "description": "Food delivery to room",
    "price": 20.00,
    "is_available": true
  }
]
```

### Add Service to Booking
```
POST /api/booking-services/
Content-Type: application/json

{
  "booking": 1,
  "service": 1,
  "quantity": 1
}
```

---

## Staff Endpoints

### List Staff
```
GET /api/staff/
```

**Query Parameters:**
- `search` - Search by name or position
- `ordering` - Order by hire_date or salary
- `position` - Filter by position

### Get Active Staff
```
GET /api/staff/active/
```

### Get Staff by Position
```
GET /api/staff/by_position/?position=Manager
```

### Create Staff
```
POST /api/staff/
Content-Type: application/json

{
  "user": 1,
  "employee_id": "EMP-001",
  "position": "Manager",
  "department": "Management",
  "shift": "Morning",
  "phone": "+1-800-HOTEL-1",
  "hire_date": "2024-01-01",
  "salary": 5000.00,
  "is_active": true
}
```

---

## Review Endpoints

### Create Review
```
POST /api/reviews/
Content-Type: application/json

{
  "booking": 1,
  "guest": 1,
  "rating": 5,
  "cleanliness": 5,
  "service": 4,
  "food": 4,
  "comment": "Great stay!",
  "would_recommend": true
}
```

### Get Average Ratings
```
GET /api/reviews/average_rating/
```

**Response:**
```json
{
  "avg_rating": 4.5,
  "avg_cleanliness": 4.7,
  "avg_service": 4.3,
  "avg_food": 4.2
}
```

---

## Maintenance Endpoints

### Create Maintenance Request
```
POST /api/maintenance-requests/
Content-Type: application/json

{
  "room": 1,
  "priority": "High",
  "description": "Broken AC unit",
  "status": "Open",
  "assigned_to": null
}
```

### Assign Maintenance
```
POST /api/maintenance-requests/{id}/assign/
Content-Type: application/json

{
  "staff_id": 1
}
```

### Complete Maintenance
```
POST /api/maintenance-requests/{id}/complete/
```

---

## Complaint Endpoints

### Create Complaint
```
POST /api/complaints/
Content-Type: application/json

{
  "booking": 1,
  "guest": 1,
  "complaint_type": "Cleanliness",
  "description": "Room not clean on arrival",
  "status": "Open"
}
```

### Resolve Complaint
```
POST /api/complaints/{id}/resolve/
Content-Type: application/json

{
  "resolution": "Room was cleaned and guest moved to another room"
}
```

---

## Status Codes

- `200 OK` - Request successful
- `201 Created` - Resource created successfully
- `204 No Content` - Request successful, no content returned
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Permission denied
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

## Error Response Example

```json
{
  "error": "Invalid data",
  "details": {
    "field_name": ["Error message"]
  }
}
```

---

## Pagination

Paginated endpoints return:

```json
{
  "count": 100,
  "next": "http://api.example.com/api/bookings/?page=2",
  "previous": null,
  "results": [...]
}
```

Add `page` parameter to navigate: `?page=2`

Set `PAGE_SIZE` in settings.py to change page size (default: 20).
