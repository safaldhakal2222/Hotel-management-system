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


async function loadBookings() {
    try {
        const res = await fetch("http://127.0.0.1:8000/api/bookings/");
        const bookings = await res.json();

        const table = document.getElementById("bookingTable");
        table.innerHTML = "";

        bookings.forEach(b => {

            let statusClass = "pending";
            if (b.status === "checked-in") statusClass = "ok";

            table.innerHTML += `
                <tr>
                    <td>${b.guest_name || "N/A"}</td>
                    <td>${b.room_number || "-"}</td>
                    <td class="${statusClass}">${b.status}</td>
                </tr>
            `;
        });

    } catch (err) {
        console.error("Booking load error:", err);
    }
}

async function loadRooms() {
    try {
        const res = await fetch("http://127.0.0.1:8000/api/rooms/");
        const rooms = await res.json();

        let available = 0;
        let occupied = 0;
        let maintenance = 0;

        rooms.forEach(room => {
            let status = room.status || "available";

            if (status === "available") available++;
            else if (status === "occupied") occupied++;
            else maintenance++;
        });

        let total = rooms.length;

        // numbers
        document.getElementById("totalRooms").innerText = total;
        document.getElementById("availableRooms").innerText = available;
        document.getElementById("occupiedRooms").innerText = occupied;
        document.getElementById("maintenanceRooms").innerText = maintenance;

        // bars (percentage)
        document.getElementById("availableBar").style.width =
            (available / total) * 100 + "%";

        document.getElementById("occupiedBar").style.width =
            (occupied / total) * 100 + "%";

        document.getElementById("maintenanceBar").style.width =
            (maintenance / total) * 100 + "%";

    } catch (error) {
        console.log("Room API Error:", error);
    }
}

const API_URL = "http://127.0.0.1:8000/api/rooms/";

async function loadRooms(){
    try{
        const response = await fetch(API_URL);
        const rooms = await response.json();

        const table = document.getElementById("roomTable");

        let total = rooms.length;
        let available = 0;
        let occupied = 0;
        let maintenance = 0;

        table.innerHTML = "";

        rooms.forEach(room => {

            let status = room.status || "available";

            if(status === "available") available++;
            else if(status === "occupied") occupied++;
            else maintenance++;

            table.innerHTML += `
                <tr>
                    <td>${room.room_number || room.id}</td>
                    <td>${room.room_type || "Standard"}</td>
                    <td class="${status === "available" ? "ok" : "pending"}">
                        ${status}
                    </td>
                    <td>$${room.price || 0}</td>
                    <td><button>View</button></td>
                </tr>
            `;
        });

        document.getElementById("totalRooms").innerText = total;
        document.getElementById("availableRooms").innerText = available;
        document.getElementById("occupiedRooms").innerText = occupied;
        document.getElementById("maintenanceRooms").innerText = maintenance;

    } catch(error){
        console.log("API Error:", error);

        document.getElementById("roomTable").innerHTML =
        "<tr><td colspan='5'>Failed to load rooms</td></tr>";
    }
}


loadRooms();
loadDashboard();
loadBookings();
loadRooms();

