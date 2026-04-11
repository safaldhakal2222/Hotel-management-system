// ============ API CONFIGURATION ============

const API_BASE = 'http://127.0.0.1:8000/api';
const API_AUTH = 'http://127.0.0.1:8000/api-auth';

// Store token in localStorage
let authToken = localStorage.getItem('authToken');

// ============ AUTHENTICATION ============

async function login(username, password) {
    try {
        const response = await fetch(`${API_BASE}/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Basic ' + btoa(username + ':' + password)
            }
        });

        if (response.ok) {
            // For session authentication, we just need to validate credentials
            localStorage.setItem('username', username);
            localStorage.setItem('password', password);
            localStorage.setItem('isLoggedIn', 'true');
            return { success: true };
        } else {
            return { success: false, error: 'Invalid credentials' };
        }
    } catch (error) {
        console.error('Login error:', error);
        return { success: false, error: error.message };
    }
}

function logout() {
    localStorage.removeItem('username');
    localStorage.removeItem('password');
    localStorage.removeItem('isLoggedIn');
    localStorage.removeItem('authToken');
    window.location.href = 'login.html';
}

function isLoggedIn() {
    return localStorage.getItem('isLoggedIn') === 'true';
}

function getAuthHeaders() {
    const username = localStorage.getItem('username');
    const password = localStorage.getItem('password');
    if (username && password) {
        return {
            'Content-Type': 'application/json',
            'Authorization': 'Basic ' + btoa(username + ':' + password)
        };
    }
    return { 'Content-Type': 'application/json' };
}

// ============ GENERIC API CALLS ============

async function apiCall(endpoint, method = 'GET', data = null) {
    const url = `${API_BASE}${endpoint}`;
    const options = {
        method,
        headers: getAuthHeaders(),
    };

    if (data) {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(url, options);
        
        if (!response.ok) {
            if (response.status === 401) {
                logout();
                throw new Error('Unauthorized. Please login again.');
            }
            throw new Error(`HTTP Error: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// ============ HOTELS ============

async function getHotels() {
    try {
        return await apiCall('/hotels/');
    } catch (error) {
        console.error('Error fetching hotels:', error);
        return [];
    }
}

async function getHotelById(id) {
    return await apiCall(`/hotels/${id}/`);
}

async function getHotelStatistics(id) {
    return await apiCall(`/hotels/${id}/statistics/`);
}

// ============ ROOMS ============

async function getRooms() {
    try {
        return await apiCall('/rooms/');
    } catch (error) {
        console.error('Error fetching rooms:', error);
        return [];
    }
}

async function getAvailableRooms(checkIn, checkOut) {
    try {
        return await apiCall(`/rooms/available/?check_in=${checkIn}&check_out=${checkOut}`);
    } catch (error) {
        console.error('Error fetching available rooms:', error);
        return [];
    }
}

async function getRoomById(id) {
    return await apiCall(`/rooms/${id}/`);
}

// ============ BOOKINGS ============

async function getBookings() {
    try {
        return await apiCall('/bookings/');
    } catch (error) {
        console.error('Error fetching bookings:', error);
        return [];
    }
}

async function getUpcomingBookings() {
    try {
        return await apiCall('/bookings/upcoming/');
    } catch (error) {
        console.error('Error fetching upcoming bookings:', error);
        return [];
    }
}

async function createBooking(bookingData) {
    return await apiCall('/bookings/', 'POST', bookingData);
}

async function getBookingById(id) {
    return await apiCall(`/bookings/${id}/`);
}

async function confirmBooking(id) {
    return await apiCall(`/bookings/${id}/confirm/`, 'POST');
}

async function checkInBooking(id) {
    return await apiCall(`/bookings/${id}/check_in/`, 'POST');
}

async function checkOutBooking(id) {
    return await apiCall(`/bookings/${id}/check_out/`, 'POST');
}

async function cancelBooking(id) {
    return await apiCall(`/bookings/${id}/cancel/`, 'POST');
}

// ============ GUESTS ============

async function getGuests() {
    try {
        return await apiCall('/guests/');
    } catch (error) {
        console.error('Error fetching guests:', error);
        return [];
    }
}

async function getGuestById(id) {
    return await apiCall(`/guests/${id}/`);
}

async function getGuestBookings(id) {
    return await apiCall(`/guests/${id}/bookings/`);
}

async function createGuest(guestData) {
    return await apiCall('/guests/', 'POST', guestData);
}

// ============ PAYMENTS ============

async function getPayments() {
    try {
        return await apiCall('/payments/');
    } catch (error) {
        console.error('Error fetching payments:', error);
        return [];
    }
}

async function getPaymentById(id) {
    return await apiCall(`/payments/${id}/`);
}

async function processPayment(id) {
    return await apiCall(`/payments/${id}/process_payment/`, 'POST');
}

// ============ SERVICES ============

async function getServices() {
    try {
        return await apiCall('/services/');
    } catch (error) {
        console.error('Error fetching services:', error);
        return [];
    }
}

// ============ REVIEWS ============

async function getReviews() {
    try {
        return await apiCall('/reviews/');
    } catch (error) {
        console.error('Error fetching reviews:', error);
        return [];
    }
}

async function getAverageRating() {
    return await apiCall('/reviews/average_rating/');
}

async function createReview(reviewData) {
    return await apiCall('/reviews/', 'POST', reviewData);
}

// ============ STAFF ============

async function getStaff() {
    try {
        return await apiCall('/staff/');
    } catch (error) {
        console.error('Error fetching staff:', error);
        return [];
    }
}

async function getActiveStaff() {
    return await apiCall('/staff/active/');
}

// ============ MAINTENANCE & COMPLAINTS ============

async function getMaintenanceRequests() {
    try {
        return await apiCall('/maintenance-requests/');
    } catch (error) {
        console.error('Error fetching maintenance requests:', error);
        return [];
    }
}

async function completeMaintenanceRequest(id) {
    return await apiCall(`/maintenance-requests/${id}/complete/`, 'POST');
}

async function getComplaints() {
    try {
        return await apiCall('/complaints/');
    } catch (error) {
        console.error('Error fetching complaints:', error);
        return [];
    }
}

async function resolveComplaint(id, resolution) {
    return await apiCall(`/complaints/${id}/resolve/`, 'POST', { resolution });
}
