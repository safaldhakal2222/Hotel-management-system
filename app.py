from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# 🔗 Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="hotel"
)

cursor = db.cursor()

# 🏠 Home route
@app.route('/')
def home():
    return "Hotel Backend Running ✅"

# 🏨 Book room
@app.route('/book', methods=['POST'])
def book_room():
    try:
        data = request.json
        name = data.get('name')
        room = data.get('room')

        query = "INSERT INTO bookings (name, room) VALUES (%s, %s)"
        cursor.execute(query, (name, room))
        db.commit()

        return jsonify({"message": "Booking successful"})
    
    except Exception as e:
        return jsonify({"error": str(e)})

# 📋 Get all bookings
@app.route('/bookings', methods=['GET'])
def get_bookings():
    cursor.execute("SELECT * FROM bookings")
    result = cursor.fetchall()

    bookings = []
    for row in result:
        bookings.append({
            "id": row[0],
            "name": row[1],
            "room": row[2]
        })

    return jsonify(bookings)

# 🚪 Get available rooms (example static)
@app.route('/rooms', methods=['GET'])
def get_rooms():
    rooms = [
        {"room": 101, "type": "Single"},
        {"room": 102, "type": "Double"},
        {"room": 103, "type": "Deluxe"}
    ]
    return jsonify(rooms)

# ❌ Delete booking (checkout)
@app.route('/checkout/<int:id>', methods=['DELETE'])
def checkout(id):
    query = "DELETE FROM bookings WHERE id = %s"
    cursor.execute(query, (id,))
    db.commit()

    return jsonify({"message": "Checked out successfully"})

# ▶ Run server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
