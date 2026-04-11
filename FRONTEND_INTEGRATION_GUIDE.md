# Frontend-Backend Integration Guide

## Setup Steps

### 1. **Install Required Packages**
Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### 2. **Migrate Database**
```bash
python manage.py migrate
```

### 3. **Create Superuser (Admin Account)**
```bash
python manage.py createsuperuser
```
Example:
- Username: `admin`
- Password: `your_secure_password`

### 4. **Run Development Server**
```bash
python manage.py runserver
```

The server will start at: `http://127.0.0.1:8000/`

---

## Accessing the Application

### Frontend
- **Login Page**: http://127.0.0.1:8000/login/
- **Dashboard**: http://127.0.0.1:8000/

### Backend
- **Django Admin**: http://127.0.0.1:8000/admin/
- **API Endpoints**: http://127.0.0.1:8000/api/

---

## API Endpoints Documentation

### Hotels
- `GET /api/hotels/` - List all hotels
- `POST /api/hotels/` - Create new hotel
- `GET /api/hotels/{id}/` - Get hotel details
- `GET /api/hotels/{id}/statistics/` - Get hotel statistics

### Rooms
- `GET /api/rooms/` - List all rooms
- `GET /api/rooms/available/?check_in=YYYY-MM-DD&check_out=YYYY-MM-DD` - Get available rooms
- `POST /api/rooms/{id}/mark_maintenance/` - Mark room for maintenance

### Bookings
- `GET /api/bookings/` - List all bookings
- `POST /api/bookings/` - Create new booking
- `GET /api/bookings/upcoming/` - Get upcoming bookings
- `POST /api/bookings/{id}/confirm/` - Confirm booking
- `POST /api/bookings/{id}/check_in/` - Check in guest
- `POST /api/bookings/{id}/check_out/` - Check out guest
- `POST /api/bookings/{id}/cancel/` - Cancel booking

### Guests
- `GET /api/guests/` - List all guests
- `POST /api/guests/` - Create new guest
- `GET /api/guests/{id}/bookings/` - Get guest bookings

### Payments
- `GET /api/payments/` - List all payments
- `POST /api/payments/{id}/process_payment/` - Process payment

### Services
- `GET /api/services/` - List available services

### Reviews
- `GET /api/reviews/` - List all reviews
- `GET /api/reviews/average_rating/` - Get average ratings
- `POST /api/reviews/` - Create new review

### Staff
- `GET /api/staff/` - List all staff
- `GET /api/staff/active/` - Get active staff

### Maintenance & Complaints
- `GET /api/maintenance-requests/` - List maintenance requests
- `POST /api/maintenance-requests/{id}/complete/` - Complete maintenance
- `GET /api/complaints/` - List complaints
- `POST /api/complaints/{id}/resolve/` - Resolve complaint

---

## Frontend Files Structure

```
HTML,CSS,JAVASCRIPT/
├── index.html           # Dashboard page
├── login.html           # Login page
├── api.js              # API helper functions (MAIN FILE FOR INTEGRATION)
├── style.css           # Dashboard styles
└── login.css           # Login styles
```

---

## How It Works

### Authentication Flow

1. **User logs in** on `login.html`
2. **JavaScript** sends credentials to Django backend using Basic Authentication
3. **Backend validates** credentials against Django User model
4. **Frontend stores** username/password in `localStorage`
5. **All API calls** automatically include authentication headers

### Data Loading

1. **Dashboard loads** and checks if user is logged in
2. **If not logged in** → redirects to login page
3. **If logged in** → fetches data from API endpoints
4. **Data is processed** and displayed in the UI
5. **Dashboard auto-refreshes** every 30 seconds

---

## Key JavaScript Functions in api.js

### Authentication
```javascript
login(username, password)          // Authenticate user
logout()                           // Clear session
isLoggedIn()                       // Check if logged in
getAuthHeaders()                   // Get auth headers for API calls
```

### Generic API Calls
```javascript
apiCall(endpoint, method, data)    // Make any API request
```

### Hotels
```javascript
getHotels()                        // List all hotels
getHotelById(id)                   // Get specific hotel
getHotelStatistics(id)             // Get hotel statistics
```

### Bookings
```javascript
getBookings()                      // List all bookings
getUpcomingBookings()              // Get upcoming bookings
createBooking(data)                // Create new booking
confirmBooking(id)                 // Confirm booking
checkInBooking(id)                 // Check in guest
checkOutBooking(id)                // Check out guest
cancelBooking(id)                  // Cancel booking
```

### Rooms
```javascript
getRooms()                         // List all rooms
getAvailableRooms(checkIn, checkOut) // Get available rooms for dates
```

### Guests
```javascript
getGuests()                        // List all guests
createGuest(data)                  // Create new guest
getGuestBookings(id)               // Get guest's bookings
```

### Payments
```javascript
getPayments()                      // List all payments
processPayment(id)                 // Process payment
```

---

## Testing the Integration

### 1. Start the server
```bash
python manage.py runserver
```

### 2. Create a test user in admin
Visit: http://127.0.0.1:8000/admin/

### 3. Go to login page
Visit: http://127.0.0.1:8000/login/

### 4. Enter your credentials
Username: `admin`
Password: `your_password`

### 5. Dashboard should load with real data

---

## Troubleshooting

### Login fails
- Check if user exists in Django admin
- Verify username and password are correct
- Check browser console for errors (F12)
- Check Django server logs

### Dashboard shows "Loading..." forever
- Check API endpoints are accessible: http://127.0.0.1:8000/api/bookings/
- Verify user is authenticated
- Check browser console for API errors (F12)
- Check Django server logs for errors

### CORS errors
- CORS is already enabled in settings.py
- Make sure you're accessing from http://127.0.0.1:8000 (not localhost)

### Static files not loading
- Run: `python manage.py collectstatic --noinput`
- Make sure DEBUG = True in settings.py

---

## Security Notes

⚠️ **For Development Only:**
- Store credentials in `localStorage` (not secure for production)
- Use Basic Authentication over HTTP (only for development)
- DEBUG = True (disable in production)

**For Production:**
- Use Token Authentication or JWT
- Store tokens securely
- Use HTTPS
- Set DEBUG = False
- Use environment variables for secrets

---

## Next Steps

1. ✅ Add more features to the frontend
2. ✅ Integrate room booking calendar
3. ✅ Add payment gateway integration
4. ✅ Create advanced reporting
5. ✅ Deploy to production server

---

**Need Help?** Check the API responses in browser developer tools (F12 → Network tab)
