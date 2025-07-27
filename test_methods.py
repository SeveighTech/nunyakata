#!/usr/bin/env python3
"""
Test different HTTP methods and headers for Nalo Solutions SMS API
"""

import requests
from urllib.parse import urlencode


def test_api_methods():
    """Test different HTTP methods and content types"""

    # SMS configuration
    config = {
        "username": "your_username",
        "password": "your_password",
        "destination": "233265542141",
        "message": "Test message",
        "source": "your_source",
        "type": "0",
        "dlr": "1",
    }

    # Test domains that were reachable
    test_urls = [
        "https://nalosolutions.com/clientapi/Resl_Nalo/send-message",
        "https://www.nalosolutions.com/clientapi/Resl_Nalo/send-message",
        "https://api.nalosolutions.com/sms/send-message",
    ]

    print("🔍 Testing different HTTP methods and content types...\n")

    for url in test_urls:
        print(f"Testing URL: {url}")

        # Test 1: POST with form data
        print("  1️⃣ POST with form data:")
        try:
            response = requests.post(url, data=config, timeout=10)
            print(f"    Status: {response.status_code}")
            if response.status_code not in [404, 500]:
                print(f"    Response: {response.text[:100]}...")
        except requests.exceptions.RequestException as e:
            print(f"    Error: {str(e)[:50]}...")

        # Test 2: POST with JSON
        print("  2️⃣ POST with JSON:")
        try:
            headers = {"Content-Type": "application/json"}
            response = requests.post(url, json=config, headers=headers, timeout=10)
            print(f"    Status: {response.status_code}")
            if response.status_code not in [404, 500]:
                print(f"    Response: {response.text[:100]}...")
        except requests.exceptions.RequestException as e:
            print(f"    Error: {str(e)[:50]}...")

        # Test 3: POST with different headers
        print("  3️⃣ POST with application/x-www-form-urlencoded:")
        try:
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            response = requests.post(url, data=config, headers=headers, timeout=10)
            print(f"    Status: {response.status_code}")
            if response.status_code not in [404, 500]:
                print(f"    Response: {response.text[:100]}...")
        except requests.exceptions.RequestException as e:
            print(f"    Error: {str(e)[:50]}...")

        # Test 4: GET with better headers
        print("  4️⃣ GET with User-Agent:")
        try:
            headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}
            response = requests.get(
                f"{url}?{urlencode(config)}", headers=headers, timeout=10
            )
            print(f"    Status: {response.status_code}")
            if response.status_code not in [404, 500]:
                print(f"    Response: {response.text[:100]}...")
        except requests.exceptions.RequestException as e:
            print(f"    Error: {str(e)[:50]}...")

        print()


if __name__ == "__main__":
    test_api_methods()
