#!/usr/bin/env python3
"""
Test SMS URL construction and connectivity
"""

import requests
from urllib.parse import urlencode


def test_sms_url():
    """Test the SMS URL construction"""

    # Test parameters matching our config
    base_url = "https://sms.nalosolutions.com"
    prefix = "Resl_Nalo"

    # Construct the URL like our code does
    sms_base_url = f"{base_url}/clientapi/{prefix}/send-message"

    print(f"📡 Testing SMS API URL: {sms_base_url}")

    # Test parameters
    sms_data = {
        "destination": "233265542141",
        "message": "Test message",
        "source": "your_source",
        "type": "0",
        "dlr": "1",
        "username": "your_username",
        "password": "your_password",
    }

    # Construct full URL with parameters
    full_url = f"{sms_base_url}?" + urlencode(sms_data)
    print(f"📱 Full URL: {full_url[:100]}...")

    # Test just the base domain first
    print(f"\n🌐 Testing base domain: {base_url}")
    try:
        response = requests.get(base_url, timeout=10)
        print(f"  ✅ Base domain status: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Base domain error: {e}")

    # Test the SMS endpoint
    print(f"\n📲 Testing SMS endpoint: {sms_base_url}")
    try:
        response = requests.get(sms_base_url, timeout=10)
        print(f"  ✅ SMS endpoint status: {response.status_code}")
        if response.text:
            print(f"  📝 Response preview: {response.text[:200]}...")
    except Exception as e:
        print(f"  ❌ SMS endpoint error: {e}")

    # Test with parameters
    print(f"\n🚀 Testing with parameters...")
    try:
        response = requests.get(full_url, timeout=10)
        print(f"  ✅ Full request status: {response.status_code}")
        if response.text:
            print(f"  📝 Response: {response.text[:500]}...")
    except Exception as e:
        print(f"  ❌ Full request error: {e}")


if __name__ == "__main__":
    test_sms_url()
