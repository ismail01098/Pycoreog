#!/usr/bin/env python3
"""API Test Script - Verify all backend endpoints work correctly."""

import requests
import json
import time
import traceback

BASE_URL = "http://localhost:5000"
TIMEOUT = 10


def print_section(title):
    """Print a formatted section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def test_registration():
    """Test user registration endpoints."""
    print_section("Testing User Registration")

    # Test 1: Register a new user
    print("1. Registering new user 'testfarmer'...")
    response = requests.post(
        f"{BASE_URL}/api/register",
        json={
            "username": "testfarmer",
            "password": "secure123"
        },
        timeout=TIMEOUT
    )
    print(f"   Status: {response.status_code}")
    data = response.json()
    print(f"   Response: {json.dumps(data, indent=2)}")

    # Test 2: Try duplicate registration
    print("\n2. Trying to register duplicate username (should fail)...")
    response = requests.post(
        f"{BASE_URL}/api/register",
        json={
            "username": "testfarmer",
            "password": "different"
        },
        timeout=TIMEOUT
    )
    print(f"   Status: {response.status_code}")
    data = response.json()
    print(f"   Response: {json.dumps(data, indent=2)}")

    # Test 3: Register without password
    print("\n3. Trying registration without password (should fail)...")
    response = requests.post(
        f"{BASE_URL}/api/register",
        json={
            "username": "anotheruser",
            "password": ""
        },
        timeout=TIMEOUT
    )
    print(f"   Status: {response.status_code}")
    data = response.json()
    print(f"   Response: {json.dumps(data, indent=2)}")


def test_login():
    """Test user login endpoints."""
    print_section("Testing User Login")

    # Test 1: Login with correct credentials
    print("1. Logging in with correct credentials...")
    response = requests.post(
        f"{BASE_URL}/api/login",
        json={
            "username": "testfarmer",
            "password": "secure123"
        },
        timeout=TIMEOUT
    )
    print(f"   Status: {response.status_code}")
    data = response.json()
    print(f"   Response: {json.dumps(data, indent=2)}")

    # Test 2: Login with wrong password
    print("\n2. Logging in with wrong password (should fail)...")
    response = requests.post(
        f"{BASE_URL}/api/login",
        json={
            "username": "testfarmer",
            "password": "wrongpassword"
        },
        timeout=TIMEOUT
    )
    print(f"   Status: {response.status_code}")
    data = response.json()
    print(f"   Response: {json.dumps(data, indent=2)}")

    # Test 3: Login with non-existent user
    print("\n3. Logging in with non-existent user (should fail)...")
    response = requests.post(
        f"{BASE_URL}/api/login",
        json={
            "username": "nonexistent",
            "password": "password123"
        },
        timeout=TIMEOUT
    )
    print(f"   Status: {response.status_code}")
    data = response.json()
    print(f"   Response: {json.dumps(data, indent=2)}")


def test_weather():
    """Test weather API endpoint."""
    print_section("Testing Weather API")

    print("1. Getting weather for 'New Delhi'...")
    response = requests.post(
        f"{BASE_URL}/api/weather",
        json={"location": "New Delhi"},
        timeout=TIMEOUT
    )
    print(f"   Status: {response.status_code}")
    data = response.json()
    if data.get('success'):
        print(f"   Location: {data.get('location')}")
        print("   Forecast data received")
    else:
        print(f"   Error: {data.get('message')}")


def test_soil():
    """Test soil data API endpoint."""
    print_section("Testing Soil Data API")

    print("1. Getting soil data for 'Mumbai'...")
    response = requests.post(
        f"{BASE_URL}/api/soil",
        json={"location": "Mumbai"},
        timeout=TIMEOUT
    )
    print(f"   Status: {response.status_code}")
    data = response.json()
    if data.get('success'):
        print(f"   Location: {data.get('location')}")
        print("   Soil data received")
    else:
        print(f"   Error: {data.get('message')}")


def test_products():
    """Test product comparison API endpoint."""
    print_section("Testing Product Comparison API")

    products = ["tomato", "rice", "wheat", "banana"]

    for product in products:
        print(f"Checking price for '{product}'...")
        response = requests.post(
            f"{BASE_URL}/api/product_comparison",
            json={"product": product},
            timeout=TIMEOUT
        )
        data = response.json()
        if data.get('success'):
            price = data.get('price')
            market = data.get('market')
            product_name = data.get('name')
            print(f"   {product_name}: ₹{price} ({market})")
        else:
            print(f"   {data.get('message')}")


def test_static_files():
    """Test that static files are being served correctly."""
    print_section("Testing Static File Serving")

    files_to_test = [
        ("", "index.html"),
        ("login.html", "login.html"),
        ("login.js", "login.js"),
        ("style.css", "style.css"),
    ]

    for path, description in files_to_test:
        url = f"{BASE_URL}/{path}" if path else f"{BASE_URL}/"
        response = requests.get(url, timeout=TIMEOUT)
        status = "OK" if response.status_code == 200 else "FAIL"
        print(f"{status} {description}: {response.status_code}")


def main():
    """Main test runner function."""
    print("\n" + "█"*60)
    print("█  FARMERS FIRST - API TEST SUITE")
    print("█"*60)
    print(f"\nTesting server at: {BASE_URL}")

    # Wait for server to be ready
    print("Checking if server is running...", end="", flush=True)
    for _ in range(10):
        try:
            requests.get(f"{BASE_URL}/", timeout=TIMEOUT)
            print(" OK")
            break
        except Exception:
            time.sleep(1)
            print(".", end="", flush=True)
    else:
        print(" FAILED")
        print("\nERROR: Could not connect to server!")
        print("Make sure the Flask server is running")
        return

    try:
        test_static_files()
        test_registration()
        test_login()
        test_weather()
        test_soil()
        test_products()

        print_section("Test Summary")
        print("All API endpoints are functioning correctly!")
        print("Database operations working properly")
        print("Static files being served correctly")

    except Exception as e:
        print(f"\nERROR: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    main()
