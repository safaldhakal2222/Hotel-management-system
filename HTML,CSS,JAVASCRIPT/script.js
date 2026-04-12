function toggleSidebar(){
    document.getElementById("sidebar").classList.toggle("active");
    document.getElementById("overlay").classList.toggle("show");
    document.getElementById("mainContent").classList.toggle("shift");
}

<<<<<<< HEAD
// ============ BOOKING FUNCTIONS ============

=======
>>>>>>> ffa2eb9b8cefe477941b5780ebd7e987f2ee3421
// Load hotels on page load
async function loadHotels() {
    try {
        const hotels = await getHotels();
        const hotelSelect = document.getElementById('hotelId');
        
        if (hotelSelect && hotels.length > 0) {
            hotels.forEach(hotel => {
                const option = document.createElement('option');
                option.value = hotel.id;
                option.textContent = hotel.name;
                hotelSelect.appendChild(option);
            });
            
            // Load rooms for first hotel
            if (hotels.length > 0) {
                await loadRoomsByHotel(hotels[0].id);
            }
        } else {
            console.warn('No hotels available');
        }
    } catch (error) {
        console.error('Error loading hotels:', error);
    }
}

// Load available rooms by hotel
async function loadRoomsByHotel(hotelId) {
    try {
        if (!hotelId) {
            document.getElementById('roomId').innerHTML = '<option value="">Select a hotel first</option>';
            return;
        }

        const rooms = await getRooms();
        const roomSelect = document.getElementById('roomId');
        
        // Clear previous options except the first one
        roomSelect.innerHTML = '<option value="">Select a room</option>';
        
        const filteredRooms = rooms.filter(room => {
            return room.hotel === parseInt(hotelId) && room.is_available && room.status === 'Available';
        });

        if (filteredRooms.length === 0) {
            roomSelect.innerHTML += '<option value="" disabled>No available rooms</option>';
            console.warn('No available rooms for hotel:', hotelId);
            return;
        }

        filteredRooms.forEach(room => {
            const option = document.createElement('option');
            option.value = room.id;
            option.textContent = `Room ${room.room_number} (${room.room_type_name}) - $${room.price_per_night}/night`;
            roomSelect.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading rooms:', error);
        alert('Error loading rooms: ' + error.message);
    }
}

// Event listener for hotel selection change
function setupHotelChangeListener() {
    const hotelSelect = document.getElementById('hotelId');
    if (hotelSelect) {
        hotelSelect.addEventListener('change', (e) => {
            loadRoomsByHotel(e.target.value);
        });
    }
}

// Create booking from form
async function createBooking() {
    try {
        // Get form values
        const hotelId = document.getElementById('hotelId')?.value;
        const firstName = document.getElementById('firstName')?.value;
        const lastName = document.getElementById('lastName')?.value;
        const email = document.getElementById('email')?.value;
        const phone = document.getElementById('phone')?.value;
        const roomId = document.getElementById('roomId')?.value;
        const numberOfGuests = document.getElementById('numberOfGuests')?.value;
        const checkInDate = document.getElementById('checkInDate')?.value;
        const checkOutDate = document.getElementById('checkOutDate')?.value;

        // Validate inputs
        if (!hotelId || !firstName || !lastName || !email || !phone || !roomId || !checkInDate || !checkOutDate) {
            alert('Please fill in all fields');
            console.warn({hotelId, firstName, lastName, email, phone, roomId, checkInDate, checkOutDate});
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
            alert('Error creating guest profile: ' + error.message);
            return;
        }

        // Create booking with hotel field
        const bookingData = {
            hotel: parseInt(hotelId),
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

// Load data when page loads
window.addEventListener('load', () => {
    loadHotels();
    setupHotelChangeListener();
});
