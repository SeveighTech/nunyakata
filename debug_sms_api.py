#!/usr/bin/env python3
"""
Test script to debug SMS API URL and connectivity
"""

import requests
from urllib.parse import urlencode


def test_sms_url():
    """Test the SMS API URL construction and connectivity"""

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

    # Base URL construction (same as in our package)
    base_url = "https://smsonline.nalosolutions.com"
    prefix = "Resl_Nalo"
    sms_base_url = f"{base_url}/clientapi/{prefix}/send-message"

    print(f"🔍 Testing SMS API connectivity...")
    print(f"Base URL: {base_url}")
    print(f"Prefix: {prefix}")
    print(f"Full SMS URL: {sms_base_url}")
    print()

    # Test 1: Check if base domain is reachable
    print("1️⃣ Testing base domain connectivity...")
    try:
        response = requests.get(base_url, timeout=10)
        print(f"   ✅ Base domain reachable - Status: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Base domain error: {str(e)}")
    print()

    # Test 2: Check the full SMS endpoint
    print("2️⃣ Testing SMS endpoint...")
    try:
        url_with_params = f"{sms_base_url}?" + urlencode(config)
        print(f"   Full URL: {url_with_params}")
        response = requests.get(url_with_params, timeout=10)
        print(f"   ✅ SMS endpoint reachable - Status: {response.status_code}")
        print(f"   Response: {response.text[:200]}...")
    except requests.exceptions.RequestException as e:
        print(f"   ❌ SMS endpoint error: {str(e)}")
    print()

    # Test 3: Try alternative URL structures
    print("3️⃣ Testing alternative URL structures...")
    alt_urls = [
        f"{base_url}/clientapi/send-message",
        f"{base_url}/api/{prefix}/send-message",
        f"{base_url}/{prefix}/send-message",
        "https://api.nalosolutions.com/sms/send-message",
    ]

    for alt_url in alt_urls:
        try:
            test_url = f"{alt_url}?" + urlencode(config)
            response = requests.get(test_url, timeout=5)
            print(f"   ✅ {alt_url} - Status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"   ❌ {alt_url} - Error: {str(e)}")


if __name__ == "__main__":
    test_sms_url()
