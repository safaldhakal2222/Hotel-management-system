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
        const response = await apiCall('/hotels/');
        // Handle both paginated and non-paginated responses
        return Array.isArray(response) ? response : (response.results || []);
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
        const response = await apiCall('/rooms/');
        // Handle both paginated and non-paginated responses
        return Array.isArray(response) ? response : (response.results || []);
    } catch (error) {
        console.error('Error fetching rooms:', error);
        return [];
    }
}

async function getAvailableRooms(checkIn, checkOut) {
    try {
        const response = await apiCall(`/rooms/available/?check_in=${checkIn}&check_out=${checkOut}`);
        // Handle both paginated and non-paginated responses
        return Array.isArray(response) ? response : (response.results || []);
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
        const response = await apiCall('/bookings/');
        // Handle both paginated and non-paginated responses
        return Array.isArray(response) ? response : (response.results || []);
    } catch (error) {
        console.error('Error fetching bookings:', error);
        return [];
    }
}

async function getUpcomingBookings() {
    try {
        const response = await apiCall('/bookings/upcoming/');
        // Handle both paginated and non-paginated responses
        return Array.isArray(response) ? response : (response.results || []);
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
        const response = await apiCall('/guests/');
        // Handle both paginated and non-paginated responses
        return Array.isArray(response) ? response : (response.results || []);
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
        const response = await apiCall('/payments/');
        // Handle both paginated and non-paginated responses
        return Array.isArray(response) ? response : (response.results || []);
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
        const response = await apiCall('/services/');
        // Handle both paginated and non-paginated responses
        return Array.isArray(response) ? response : (response.results || []);
    } catch (error) {
        console.error('Error fetching services:', error);
        return [];
    }
}

// ============ REVIEWS ============

async function getReviews() {
    try {
        const response = await apiCall('/reviews/');
        // Handle both paginated and non-paginated responses
        return Array.isArray(response) ? response : (response.results || []);
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
        const response = await apiCall('/staff/');
        // Handle both paginated and non-paginated responses
        return Array.isArray(response) ? response : (response.results || []);
    } catch (error) {
        console.error('Error fetching staff:', error);
        return [];
    }
}

async function getActiveStaff() {
    const response = await apiCall('/staff/active/');
    // Handle both paginated and non-paginated responses
    return Array.isArray(response) ? response : (response.results || []);
}

// ============ MAINTENANCE & COMPLAINTS ============

async function getMaintenanceRequests() {
    try {
        const response = await apiCall('/maintenance-requests/');
        // Handle both paginated and non-paginated responses
        return Array.isArray(response) ? response : (response.results || []);
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
        const response = await apiCall('/complaints/');
        // Handle both paginated and non-paginated responses
        return Array.isArray(response) ? response : (response.results || []);
    } catch (error) {
        console.error('Error fetching complaints:', error);
        return [];
    }
}

async function resolveComplaint(id, resolution) {
    return await apiCall(`/complaints/${id}/resolve/`, 'POST', { resolution });
}
