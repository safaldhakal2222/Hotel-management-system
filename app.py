from flask import Flask
from routes.booking import booking_routes

app = Flask(__name__)

app.register_blueprint(booking_routes)

if __name__ == '__main__':
    app.run(debug=True)
