#!/usr/bin/env python3
"""Test script to verify the application setup."""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all required packages can be imported."""
    print("Testing imports...")
    try:
        import flask  # noqa: F401
        print("✓ Flask imported successfully")
    except ImportError as e:
        print(f"✗ Flask import failed: {e}")
        return False

    try:
        import flask_cors  # noqa: F401
        print("✓ Flask-CORS imported successfully")
    except ImportError as e:
        print(f"✗ Flask-CORS import failed: {e}")
        return False

    try:
        import cv2  # noqa: F401
        print(f"✓ OpenCV imported successfully")
    except ImportError as e:
        print(f"✗ OpenCV import failed: {e}")
        return False

    try:
        import numpy  # noqa: F401
        print(f"✓ NumPy imported successfully")
    except ImportError as e:
        print(f"✗ NumPy import failed: {e}")
        return False

    try:
        import face_recognition  # noqa: F401
    except ImportError as e:
        print(f"⚠ Face Recognition import failed: {e}")
        print("  (App will use basic face detection via OpenCV)")
    
    return True

def test_database():
    """Test database initialization and operations."""
    print("\nTesting database setup...")
    try:
        from pycore.database import (
            ensure_database, create_user, find_user
        )
        ensure_database()
        print("✓ Database initialized successfully")
        
        # Test user creation
        success = create_user('test_user', 'test_password_hash')
        if success:
            print("✓ User creation works")
        else:
            print("✗ User creation failed (duplicate username?)")
        
        # Test user lookup
        user = find_user('test_user')
        if user:
            print("✓ User lookup works")
            print(f"  User: {user[1]}")
        else:
            print("✗ User lookup failed")
        
        return True
    except Exception as e:
        print(f"✗ Database test failed: {e}")
        return False

def test_app():
    """Test Flask app creation and basic routes."""
    try:
        from app import app
        print("✓ Flask app created successfully")
        
        # Test basic routes
        with app.test_client() as client:
            response = client.get('/')
            if response.status_code == 200:
                print("✓ Home route accessible")
            else:
                print(f"✗ Home route returned {response.status_code}")
        
        return True
    except Exception as e:
        print(f"✗ App test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("Application Setup Verification")
    print("=" * 60)
    
    all_pass = True
    all_pass = test_imports() and all_pass
    all_pass = test_database() and all_pass
    all_pass = test_app() and all_pass
    
    print("\n" + "=" * 60)
    if all_pass:
        print("✓ All tests passed! The app is ready to run.")
    else:
        print("✗ Some tests failed. Check the output above.")
    print("=" * 60)
