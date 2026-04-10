# Hotel Management System

A comprehensive Django-based hotel management system with REST API, featuring room management, booking system, payment processing, staff management, and guest reviews.

## Authors
- Safal Dhakal
- Sandesh Adhikari
- Sandesh Acharya

## Features

### 🏨 Hotel Management
- Multiple hotel management support
- Hotel information and statistics
- Revenue tracking and reporting

### 🛏️ Room Management
- Room inventory management
- Room types (Single, Double, Suite, Deluxe, etc.)
- Room status tracking (Available, Occupied, Maintenance, Reserved)
- Availability calendar

### 👥 Guest Management
- Guest profiles with identification
- Booking history
- Guest statistics and analytics

### 📅 Booking System
- Online booking with date availability checking
- Automatic booking ID generation
- Number of nights calculation
- Special notes and requirements

### 💳 Payment Processing
- Multiple payment methods (Credit Card, Debit Card, Cash, Bank Transfer, Online)
- Payment status tracking (Pending, Completed, Failed, Refunded)
- Transaction ID generation
- Automatic invoice calculation

### 👨‍💼 Staff Management
- Employee profiles and positions
- Shift management (Morning, Evening, Night)
- Department tracking
- Salary management

### 🛎️ Services & Amenities
- Room service management
- Laundry service
- Spa, Gym, Restaurant services
- Additional services tracking
- Price management per service

### ⭐ Reviews & Ratings
- Guest reviews and rating system
- Multiple rating categories (cleanliness, service, food)
- Recommendation tracking

### 🔧 Maintenance Management
- Maintenance request tracking
- Priority levels (Low, Medium, High, Urgent)
- Staff assignment
- Completion tracking

### 📝 Complaint Management
- Guest complaint tracking
- Complaint categorization
- Resolution tracking
- Status management

## Technology Stack

- **Backend**: Django 6.0.4
- **API**: Django REST Framework 3.14.0
- **Database**: SQLite (default) / PostgreSQL (production)
- **Middleware**: django-cors-headers 4.3.1
- **Python**: 3.8+

## Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd "Hotel-management-system"
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv myenv
myenv\Scripts\activate

# macOS/Linux
python3 -m venv myenv
source myenv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Initialize System
```bash
python manage.py init_hotel --hotel-name "Your Hotel Name" --admin-username "admin"
```

### 6. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 7. Run Development Server
```bash
python manage.py runserver
```

Server will be available at `http://localhost:8000`

## API Endpoints

### Hotel Management
- `GET/POST /api/hotels/` - List/Create hotels
- `GET/PUT/DELETE /api/hotels/{id}/` - Retrieve/Update/Delete hotel
- `GET /api/hotels/{id}/statistics/` - Get hotel statistics

### Rooms
- `GET/POST /api/rooms/` - List/Create rooms
- `GET /api/rooms/available/` - Get available rooms
- `POST /api/rooms/{id}/mark_maintenance/` - Mark room for maintenance

### Room Types
- `GET/POST /api/room-types/` - List/Create room types

### Guests
- `GET/POST /api/guests/` - List/Create guests
- `GET /api/guests/{id}/bookings/` - Get guest bookings

### Bookings
- `GET/POST /api/bookings/` - List/Create bookings
- `POST /api/bookings/{id}/confirm/` - Confirm booking
- `POST /api/bookings/{id}/check_in/` - Check in guest
- `POST /api/bookings/{id}/check_out/` - Check out guest
- `POST /api/bookings/{id}/cancel/` - Cancel booking
- `GET /api/bookings/upcoming/` - Get upcoming bookings

### Payments
- `GET/POST /api/payments/` - List/Create payments
- `POST /api/payments/{id}/process_payment/` - Process payment

### Services
- `GET/POST /api/services/` - List/Create services
- `GET/POST /api/booking-services/` - Add services to booking

### Staff
- `GET/POST /api/staff/` - List/Create staff
- `GET /api/staff/active/` - Get active staff
- `GET /api/staff/by_position/?position=Manager` - Get staff by position

### Reviews
- `GET/POST /api/reviews/` - List/Create reviews
- `GET /api/reviews/average_rating/` - Get average ratings

### Maintenance
- `GET/POST /api/maintenance-requests/` - List/Create maintenance requests
- `POST /api/maintenance-requests/{id}/assign/` - Assign maintenance
- `POST /api/maintenance-requests/{id}/complete/` - Complete maintenance

### Complaints
- `GET/POST /api/complaints/` - List/Create complaints
- `POST /api/complaints/{id}/resolve/` - Resolve complaint

## Admin Interface

Access the Django admin panel at `http://localhost:8000/admin/`

Login with the superuser credentials you created.

### Admin Features
- Manage all hotel data
- Create and edit bookings
- Process payments
- Manage staff and roles
- View reports and statistics
- Handle maintenance requests and complaints

## Usage Examples

### 1. Create a Booking
```bash
curl -X POST http://localhost:8000/api/bookings/ \
  -H "Content-Type: application/json" \
  -d '{
    "hotel": 1,
    "guest": 1,
    "room": 1,
    "check_in_date": "2024-01-15",
    "check_out_date": "2024-01-18",
    "number_of_guests": 2,
    "notes": "Late arrival expected"
  }'
```

### 2. Get Available Rooms
```bash
curl "http://localhost:8000/api/rooms/available/?check_in=2024-01-15&check_out=2024-01-18"
```

### 3. Process a Payment
```bash
curl -X POST http://localhost:8000/api/payments/1/process_payment/ \
  -H "Content-Type: application/json"
```

### 4. Check In a Guest
```bash
curl -X POST http://localhost:8000/api/bookings/1/check_in/ \
  -H "Content-Type: application/json"
```

## Database Models

### Hotel
- name, address, city, state, postal_code, phone, email, website, total_rooms

### Room
- room_number, room_type, floor, status, price_per_night, is_available, description

### Guest
- user, first_name, last_name, email, phone, address, city, country, postal_code, gender, id_type, id_number, date_of_birth

### Booking
- booking_id, hotel, guest, room, check_in_date, check_out_date, number_of_guests, status, number_of_nights, total_price

### Payment
- booking, amount, payment_method, status, transaction_id

### Staff
- user, employee_id, position, department, shift, phone, hire_date, salary, is_active

### Service & BookingService
- name, service_type, description, price

### Review
- booking, guest, rating, cleanliness, service, food, comment, would_recommend

### MaintenanceRequest
- room, priority, description, status, assigned_to

### Complaint
- booking, guest, complaint_type, description, status, resolution

## Utility Functions

The system includes utility functions in `resultapp/utils.py` for:
- Booking calculations
- Availability checking
- Revenue analysis
- Occupancy rate calculation
- Staff and guest statistics
- Report generation

Example:
```python
from resultapp.utils import *

# Calculate booking cost
cost = calculate_booking_cost(room, check_in, check_out)

# Get available rooms
available = get_available_rooms(check_in, check_out)

# Get hotel statistics
stats = generate_daily_report(hotel)

# Revenue calculations
revenue = get_revenue(hotel)
adr = get_average_daily_rate(hotel)
revpar = get_revpar(hotel)
```

## Testing

Run tests with:
```bash
python manage.py test
```

## Development

### Create Migration
```bash
python manage.py makemigrations
python manage.py migrate
```

### Create Superuser
```bash
python manage.py createsuperuser
```

### Run Development Server
```bash
python manage.py runserver
```

## Security Considerations

- Change `SECRET_KEY` in production
- Set `DEBUG = False` in production
- Use environment variables for sensitive data
- Configure allowed hosts properly
- Implement proper authentication and authorization
- Use HTTPS in production
- Set up CORS properly for your frontend

## Future Enhancements

- Email notifications for bookings
- SMS alerts
- Advanced reporting and analytics
- Multi-language support
- Mobile app integration
- Loyalty program management
- Advanced payment gateway integration
- AI-based pricing recommendations

## License

This project is open source and available under the MIT License.

## Support

For issues and questions, please open an issue in the repository.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

