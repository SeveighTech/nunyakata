#!/usr/bin/env python3
"""
Test various SMS endpoint paths on api.nalosolutions.com
"""

import requests
from urllib.parse import urlencode


def test_api_paths():
    """Test different path combinations on api.nalosolutions.com"""

    base_url = "https://api.nalosolutions.com"

    # Test different path variations
    paths = [
        "/smsbackend/clientapi/Resl_Nalo/send-message",
        "/smsbackend/clientapi/send-message",
        "/smsbackend/send-message",
        "/sms/clientapi/Resl_Nalo/send-message",
        "/sms/clientapi/send-message",
        "/sms/send-message",
        "/clientapi/Resl_Nalo/send-message",
        "/clientapi/send-message",
        "/send-message",
        "/sms",
        "/smsbackend",
        "/clientapi",
    ]

    print(f"🔍 Testing SMS endpoint paths on {base_url}")
    print(f"{'='*60}")

    for path in paths:
        full_url = base_url + path
        try:
            print(f"\n📱 Testing: {path}")
            response = requests.get(full_url, timeout=5)
            print(f"    Status: {response.status_code}")

            if response.status_code != 404:
                print(f"    Response preview: {response.text[:100]}...")

        except Exception as e:
            print(f"    Error: {str(e)[:50]}...")

    print(f"\n{'='*60}")
    print("🎯 Testing with SMS parameters...")

    # Test with actual SMS parameters
    sms_data = {
        "destination": "233265542141",
        "message": "Test message",
        "source": "your_source",
        "type": "0",
        "dlr": "1",
        "username": "your_username",
        "password": "your_password",
    }

    # Test the most likely paths with parameters
    likely_paths = [
        "/smsbackend/clientapi/Resl_Nalo/send-message",
        "/sms/send-message",
        "/clientapi/send-message",
    ]

    for path in likely_paths:
        try:
            full_url = f"{base_url}{path}?" + urlencode(sms_data)
            print(f"\n🚀 Testing with params: {path}")
            response = requests.get(full_url, timeout=10)
            print(f"    Status: {response.status_code}")
            if response.text and response.status_code != 404:
                print(f"    Response: {response.text[:200]}...")
        except Exception as e:
            print(f"    Error: {str(e)[:50]}...")


if __name__ == "__main__":
    test_api_paths()
