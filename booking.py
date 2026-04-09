from flask import Blueprint, request, jsonify
from db import get_db

booking_routes = Blueprint('booking', __name__)

@booking_routes.route('/book', methods=['POST'])
def book_room():
    data = request.json
    name = data.get('name')
    room = data.get('room')

    db = get_db()
    cursor = db.cursor()

    query = "INSERT INTO bookings (name, room) VALUES (%s, %s)"
    cursor.execute(query, (name, room))
    db.commit()

    return jsonify({"message": "Booking successful"})
