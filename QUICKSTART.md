# Quick Start Guide - Hotel Management System

## 5-Minute Setup

### Step 1: Install Dependencies
```bash
# Activate virtual environment
myenv\Scripts\activate  # Windows
# or
source myenv/bin/activate  # macOS/Linux

# Install packages
pip install -r requirements.txt
```

### Step 2: Setup Database
```bash
# Create database tables
python manage.py makemigrations
python manage.py migrate

# Initialize system with sample data
python manage.py init_hotel --hotel-name "Your Hotel" --admin-username "admin"
```

### Step 3: Start Server
```bash
python manage.py runserver
```

### Step 4: Login to Admin
- Open browser to `http://localhost:8000/admin/`
- Username: `admin`
- Password: `admin123`

---

## Basic Workflows

### Create and Manage a Booking

#### 1. Create a Guest
```bash
curl -X POST http://localhost:8000/api/guests/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Smith",
    "email": "john@example.com",
    "phone": "+1-555-0123",
    "country": "USA"
  }'
```

#### 2. Check Available Rooms
```bash
curl "http://localhost:8000/api/rooms/available/?check_in=2024-02-01&check_out=2024-02-05"
```

#### 3. Create Booking
```bash
curl -X POST http://localhost:8000/api/bookings/ \
  -H "Content-Type: application/json" \
  -d '{
    "hotel": 1,
    "guest": 1,
    "room": 1,
    "check_in_date": "2024-02-01",
    "check_out_date": "2024-02-05",
    "number_of_guests": 2,
    "notes": "Business trip"
  }'
```

#### 4. Confirm Booking
```bash
curl -X POST http://localhost:8000/api/bookings/1/confirm/
```

#### 5. Process Payment
```bash
curl -X POST http://localhost:8000/api/payments/1/process_payment/
```

#### 6. Check In Guest
```bash
curl -X POST http://localhost:8000/api/bookings/1/check_in/
```

#### 7. Check Out Guest
```bash
curl -X POST http://localhost:8000/api/bookings/1/check_out/
```

---

## Admin Interface Features

### Dashboard
- View hotel statistics
- Monitor room availability
- Track upcoming bookings
- Check revenue

### Manage Rooms
1. Go to admin → Rooms
2. Add new room or edit existing
3. Set room type, price, and status
4. Monitor occupancy

### Manage Bookings
1. Go to admin → Bookings
2. View all bookings with filters
3. Change booking status
4. Add notes

### Manage Guests
1. Go to admin → Guests
2. View guest information
3. Check booking history
4. Update guest details

### Manage Staff
1. Go to admin → Staff
2. Add new staff member
3. Assign shifts and positions
4. Track employment details

### Handle Complaints
1. Go to admin → Complaints
2. View open complaints
3. Add resolution
4. Mark as resolved

---

## API Quick Reference

### Most Used Endpoints

**Get Available Rooms**
```
GET /api/rooms/available/?check_in=YYYY-MM-DD&check_out=YYYY-MM-DD
```

**Create Booking**
```
POST /api/bookings/
{
  "hotel": 1,
  "guest": 1,
  "room": 1,
  "check_in_date": "2024-02-01",
  "check_out_date": "2024-02-05",
  "number_of_guests": 2
}
```

**Check Booking Status**
```
GET /api/bookings/{booking_id}/
```

**Get Upcoming Bookings**
```
GET /api/bookings/upcoming/
```

**Process Payment**
```
POST /api/payments/{payment_id}/process_payment/
```

---

## Common Tasks

### Add a New Hotel

Via Admin Interface:
1. Go to Admin → Hotels
2. Click "Add hotel"
3. Fill in details
4. Save

Via API:
```bash
curl -X POST http://localhost:8000/api/hotels/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "New Hotel",
    "address": "123 Main St",
    "city": "Boston",
    "state": "MA",
    "phone": "+1-617-555-0123",
    "email": "info@hotel.com",
    "total_rooms": 50
  }'
```

### Add Rooms to Hotel

Via Admin Interface:
1. Go to Admin → Rooms
2. Click "Add room"
3. Select hotel, room number, type
4. Set price and floor
5. Save

### Create Room Types

Via Admin Interface:
1. Go to Admin → Room types
2. Click "Add room type"
3. Enter name, capacity, base price
4. Save

**Room Types to Create:**
- Single (capacity: 1, price: $100)
- Double (capacity: 2, price: $150)
- Suite (capacity: 4, price: $250)

### Add Services

Via Admin Interface:
1. Go to Admin → Services
2. Click "Add service"
3. Enter name, type, price
4. Save

**Common Services:**
- Room Service - $20
- Laundry - $15
- Spa - $100
- Gym Access - Free
- Restaurant - Variable

### Staff Management

Add Staff:
1. First create a User account (Admin → Users)
2. Then create Staff record linking to that user
3. Set position, shift, and salary

### Generate Reports

Use utility functions in Python shell:
```python
python manage.py shell
>>> from resultapp.utils import *
>>> from resultapp.models import Hotel
>>> hotel = Hotel.objects.first()
>>> print(get_revenue(hotel))
>>> print(get_occupancy_rate(hotel))
>>> print(generate_daily_report(hotel))
```

---

## Troubleshooting

### Database Errors
```bash
# Delete and recreate database
rm db.sqlite3
python manage.py migrate
python manage.py init_hotel
```

### Port Already in Use
```bash
# Use different port
python manage.py runserver 8001
```

### Migration Issues
```bash
# Create migrations
python manage.py makemigrations
python manage.py migrate --run-syncdb
```

### Admin Access Lost
```bash
# Create new superuser
python manage.py createsuperuser
```

---

## Performance Tips

1. **Database Optimization**
   - Use indexes on frequently searched fields
   - Migrate to PostgreSQL for production

2. **API Optimization**
   - Use pagination for large datasets
   - Cache common queries
   - Use select_related() and prefetch_related()

3. **Server Optimization**
   - Use Gunicorn for production
   - Set up Nginx reverse proxy
   - Enable gzip compression

---

## Next Steps

1. Read full [API Documentation](API_DOCUMENTATION.md)
2. Explore Django Admin interface
3. Customize models if needed
4. Set up frontend application
5. Configure production settings

---

## Getting Help

- Check README.md for full features
- Review API_DOCUMENTATION.md for API details
- Check Django REST Framework docs: https://www.django-rest-framework.org/
- Check Django docs: https://docs.djangoproject.com/

---

## Security Checklist

Before production:
- [ ] Change SECRET_KEY in settings.py
- [ ] Set DEBUG = False
- [ ] Configure ALLOWED_HOSTS
- [ ] Set up HTTPS/SSL
- [ ] Configure CORS properly
- [ ] Use environment variables for secrets
- [ ] Set up database backups
- [ ] Configure logging
- [ ] Enable CSRF protection
- [ ] Set secure cookie flags

---

Happy coding! 🚀
