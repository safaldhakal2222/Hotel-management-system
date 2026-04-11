function toggleSidebar(){
    document.getElementById("sidebar").classList.toggle("active");
    document.getElementById("overlay").classList.toggle("show");
    document.getElementById("mainContent").classList.toggle("shift");
}

// ============ BOOKING FUNCTIONS ============

// Load available rooms on page load
async function loadAvailableRooms() {
    try {
        const rooms = await getRooms();
        const roomSelect = document.getElementById('roomId');
        
        if (roomSelect) {
            rooms.forEach(room => {
                if (room.is_available && room.status === 'Available') {
                    const option = document.createElement('option');
                    option.value = room.id;
                    option.textContent = `Room ${room.room_number} (${room.room_type_name}) - $${room.price_per_night}/night`;
                    roomSelect.appendChild(option);
                }
            });
        }
    } catch (error) {
        console.error('Error loading rooms:', error);
    }
}

// Create booking from form
async function createBooking() {
    try {
        // Get form values
        const firstName = document.getElementById('firstName')?.value;
        const lastName = document.getElementById('lastName')?.value;
        const email = document.getElementById('email')?.value;
        const phone = document.getElementById('phone')?.value;
        const roomId = document.getElementById('roomId')?.value;
        const numberOfGuests = document.getElementById('numberOfGuests')?.value;
        const checkInDate = document.getElementById('checkInDate')?.value;
        const checkOutDate = document.getElementById('checkOutDate')?.value;

        // Validate inputs
        if (!firstName || !lastName || !email || !phone || !roomId || !checkInDate || !checkOutDate) {
            alert('Please fill in all fields');
            return;
        }

        if (new Date(checkOutDate) <= new Date(checkInDate)) {
            alert('Check-out date must be after check-in date');
            return;
        }

        // Create guest first
        const guestData = {
            first_name: firstName,
            last_name: lastName,
            email: email,
            phone: phone,
            country: 'Unknown'
        };

        let guestId;
        try {
            const guestResponse = await createGuest(guestData);
            guestId = guestResponse.id;
        } catch (error) {
            console.error('Error creating guest:', error);
            alert('Error creating guest profile');
            return;
        }

        // Create booking
        const bookingData = {
            guest: guestId,
            room: parseInt(roomId),
            check_in_date: checkInDate,
            check_out_date: checkOutDate,
            number_of_guests: parseInt(numberOfGuests),
            notes: ''
        };

        const response = await createBooking(bookingData);
        
        alert(`Booking created successfully! Booking ID: ${response.booking_id}`);
        
        // Reset form
        document.querySelector('form')?.reset() || location.reload();
        
    } catch (error) {
        console.error('Error creating booking:', error);
        alert('Error creating booking: ' + (error.message || 'Unknown error'));
    }
}

// Load rooms when page loads
window.addEventListener('load', loadAvailableRooms);
