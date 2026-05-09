"""Farmers First - Flask backend for agricultural platform.

This module provides API endpoints for user authentication, face detection,
weather forecasts, soil data, and agricultural product pricing.
"""
import hashlib
import importlib
import os
import io
from urllib.parse import quote

import requests
import base64

opencv_available = False
face_recognition_available = False
cv2 = None
np = None
face_recognition = None

try:
    cv2 = importlib.import_module('cv2')
    np = importlib.import_module('numpy')
    opencv_available = True
except ImportError:
    cv2 = None
    np = None

try:
    face_recognition = importlib.import_module('face_recognition')
    face_recognition_available = True
except ImportError:
    face_recognition = None

if not face_recognition_available:
    print("Warning: Advanced face recognition not available. "
          "Using basic face detection if available.")

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from pycore.database import create_user, find_user, find_user_by_face, ensure_database

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, 'frontnd')

app = Flask(
    __name__,
    static_folder=FRONTEND_DIR,
    static_url_path=''
)

# Enable CORS for all routes
CORS(app)

ensure_database()


def hash_password(password: str) -> str:
    """Hash a password using SHA256.

    Args:
        password: The password string to hash.

    Returns:
        The hexadecimal hash of the password.
    """
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def detect_face_basic(image_data):
    """Detect faces using OpenCV Haar cascades.

    Args:
        image_data: Base64-encoded image data.

    Returns:
        True if a face is detected, False otherwise.
    """
    if not opencv_available or np is None or cv2 is None:
        return False

    try:
        # Decode base64 image
        image_bytes = base64.b64decode(image_data.split(',')[1])
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            return False

        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Load Haar cascade
        cascade_path = (
            cv2.data.haarcascades
            + 'haarcascade_frontalface_default.xml'
        )
        face_cascade = cv2.CascadeClassifier(cascade_path)

        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        return len(faces) > 0
    except (IndexError, AttributeError, OSError):
        return False


@app.route('/')
def index():
    """Serve the login page."""
    return send_from_directory(FRONTEND_DIR, 'login.html')


@app.route('/<path:path>')
def static_proxy(path):
    """Serve static frontend files."""
    return send_from_directory(FRONTEND_DIR, path)


@app.route('/api/login', methods=['POST'])
def api_login():
    """Handle user login with username and password."""
    data = request.get_json() or {}
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    if not username or not password:
        msg = 'Username and password are required.'
        return jsonify(success=False, message=msg)

    user = find_user(username)
    if not user:
        msg = 'Invalid username or password.'
        return jsonify(success=False, message=msg)

    _, _, password_hash, _ = user
    if hash_password(password) != password_hash:
        msg = 'Invalid username or password.'
        return jsonify(success=False, message=msg)

    return jsonify(success=True, message='Login successful.')


@app.route('/api/register', methods=['POST'])
def api_register():
    """Handle user registration with optional face encoding."""
    data = request.get_json() or {}
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    face_image = data.get('face_image')  # base64 string
    if not username or not password:
        msg = 'Username and password are required.'
        return jsonify(success=False, message=msg)

    password_hash = hash_password(password)
    face_encoding = None

    if face_image:
        if face_recognition_available:
            try:
                img_data = base64.b64decode(face_image.split(',')[1])
                img = face_recognition.load_image_file(
                    io.BytesIO(img_data)
                )
                encodings = face_recognition.face_encodings(img)
                if encodings:
                    face_encoding = encodings[0]
            except (IndexError, AttributeError, OSError, ValueError):
                msg = 'Face processing failed.'
                return jsonify(success=False, message=msg)
        elif opencv_available:
            # Basic face detection - store face was provided
            if detect_face_basic(face_image):
                # Simple marker
                face_encoding = "basic_face_detected"
            else:
                msg = 'No face detected in image.'
                return jsonify(success=False, message=msg)
        else:
            msg = ('Face recognition not available. '
                   'Use text registration only.')
            return jsonify(success=False, message=msg)

    created = create_user(username, password_hash, face_encoding)
    if not created:
        msg = 'Username already exists.'
        return jsonify(success=False, message=msg)

    msg = 'Registration successful. You can now login.'
    return jsonify(success=True, message=msg)


@app.route('/api/face_login', methods=['POST'])
def api_face_login():
    """Handle face-based login."""
    if not opencv_available and not face_recognition_available:
        msg = 'Face recognition not available.'
        return jsonify(success=False, message=msg)

    data = request.get_json() or {}
    face_image = data.get('face_image')
    if not face_image:
        msg = 'Face image is required.'
        return jsonify(success=False, message=msg)

    if face_recognition_available:
        try:
            img_data = base64.b64decode(face_image.split(',')[1])
            img = face_recognition.load_image_file(
                io.BytesIO(img_data)
            )
            encodings = face_recognition.face_encodings(img)
            if not encodings:
                msg = 'No face detected.'
                return jsonify(success=False, message=msg)

            username = find_user_by_face(encodings[0])
            if username:
                msg = 'Face login successful.'
                return jsonify(
                    success=True,
                    message=msg,
                    username=username
                )
            else:
                msg = 'Face not recognized.'
                return jsonify(success=False, message=msg)
        except (ValueError, IndexError, AttributeError, OSError):
            msg = 'Face processing failed.'
            return jsonify(success=False, message=msg)
    elif opencv_available:
        # Basic face detection - check if face is present
        if detect_face_basic(face_image):
            # For basic version, success for any registered user
            msg = 'Face detected! Login successful.'
            return jsonify(
                success=True,
                message=msg,
                username='demo_user'
            )
        else:
            msg = 'No face detected.'
            return jsonify(success=False, message=msg)

    msg = 'Face processing failed.'
    return jsonify(success=False, message=msg)


@app.route('/api/weather', methods=['POST'])
def api_weather():
    """Get weather forecast for a location."""
    data = request.get_json() or {}
    location = data.get('location', '').strip()
    if not location:
        msg = 'Location is required.'
        return jsonify(success=False, message=msg)

    geo_url = (
        'https://geocoding-api.open-meteo.com/v1/search'
        f'?name={quote(location)}&count=1&language=en&format=json'
    )
    geo = requests.get(geo_url, timeout=10).json()
    results = geo.get('results') or []
    if not results:
        msg = 'Location not found.'
        return jsonify(success=False, message=msg)

    place = results[0]
    lat = place['latitude']
    lon = place['longitude']
    forecast_url = (
        'https://api.open-meteo.com/v1/forecast'
        f'?latitude={lat}&longitude={lon}'
        '&daily=weathercode,temperature_2m_max,temperature_2m_min'
        '&timezone=auto'
    )
    forecast = requests.get(forecast_url, timeout=10).json()
    location_str = f"{place['name']}, {place['country']}"
    return jsonify(
        success=True,
        location=location_str,
        forecast=forecast
    )


@app.route('/api/soil', methods=['POST'])
def api_soil():
    """Get soil data for a location."""
    data = request.get_json() or {}
    location = data.get('location', '').strip()
    if not location:
        msg = 'Location is required.'
        return jsonify(success=False, message=msg)

    geo_url = (
        'https://geocoding-api.open-meteo.com/v1/search'
        f'?name={quote(location)}&count=1&language=en&format=json'
    )
    geo = requests.get(geo_url, timeout=10).json()
    results = geo.get('results') or []
    if not results:
        msg = 'Location not found.'
        return jsonify(success=False, message=msg)

    place = results[0]
    lat = place['latitude']
    lon = place['longitude']
    soil_url = (
        'https://api.open-meteo.com/v1/forecast'
        f'?latitude={lat}&longitude={lon}'
        '&hourly=soil_moisture_0_1cm&timezone=auto'
    )
    soil = requests.get(soil_url, timeout=10).json()
    location_str = f"{place['name']}, {place['country']}"
    return jsonify(success=True, location=location_str, soil=soil)


@app.route('/api/product_comparison', methods=['POST'])
def api_product_comparison():
    """Get product price information."""
    data = request.get_json() or {}
    product = data.get('product', '').strip().lower()
    if not product:
        msg = 'Product name is required.'
        return jsonify(success=False, message=msg)

    price_catalog = {
        'tomato': {
            'name': 'Tomato',
            'price': 28,
            'market': 'All India',
            'image': 'assets/market.svg'
        },
        'onion': {
            'name': 'Onion',
            'price': 32,
            'market': 'All India',
            'image': 'assets/market.svg'
        },
        'rice': {
            'name': 'Rice',
            'price': 45,
            'market': 'All India',
            'image': 'assets/market.svg'
        },
        'wheat': {
            'name': 'Wheat',
            'price': 26,
            'market': 'All India',
            'image': 'assets/market.svg'
        },
        'potato': {
            'name': 'Potato',
            'price': 18,
            'market': 'All India',
            'image': 'assets/market.svg'
        },
        'banana': {
            'name': 'Banana',
            'price': 35,
            'market': 'All India',
            'image': 'assets/market.svg'
        },
        'apple': {
            'name': 'Apple',
            'price': 80,
            'market': 'All India',
            'image': 'assets/market.svg'
        },
        'mango': {
            'name': 'Mango',
            'price': 95,
            'market': 'All India',
            'image': 'assets/market.svg'
        }
    }

    if product not in price_catalog:
        msg = (
            'Product not found. Try Tomato, Onion, Rice, Wheat, '
            'Potato, Banana, Apple, or Mango.'
        )
        return jsonify(success=False, message=msg)

    return jsonify(success=True, **price_catalog[product])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # pragma: no cover
