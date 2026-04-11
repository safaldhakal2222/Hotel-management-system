function toggleSidebar(){
    document.getElementById("sidebar").classList.toggle("active");
    document.getElementById("overlay").classList.toggle("show");
    document.getElementById("mainContent").classList.toggle("shift");
}

async function loadDashboard() {
    try {
        // ROOMS
        let roomRes = await fetch("http://127.0.0.1:8000/api/rooms/");
        let roomData = await roomRes.json();
        document.getElementById("totalRooms").innerText = roomData.length;

        // BOOKINGS
        let bookingRes = await fetch("http://127.0.0.1:8000/api/bookings/");
        let bookingData = await bookingRes.json();
        document.getElementById("totalBookings").innerText = bookingData.length;

        // CUSTOMERS
        let guestRes = await fetch("http://127.0.0.1:8000/api/guests/");
        let guestData = await guestRes.json();
        document.getElementById("totalCustomers").innerText = guestData.length;

        // REVENUE
        let payRes = await fetch("http://127.0.0.1:8000/api/payments/");
        let payData = await payRes.json();

        let total = 0;
        payData.forEach(p => total += p.amount);
        document.getElementById("totalRevenue").innerText = "$" + total;

    } catch (error) {
        console.error("Error loading dashboard:", error);
    }
}

// Run on load
loadDashboard();