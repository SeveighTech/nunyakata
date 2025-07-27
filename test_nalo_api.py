#!/usr/bin/env python3
"""
Test script to check Nalo Solutions API endpoints
"""

import requests


def test_endpoints():
    """Test various possible Nalo Solutions API endpoints"""

    base_urls = [
        "https://api.nalosolutions.com",
        "https://nalosolutions.com/api",
        "https://www.nalosolutions.com/api",
        "https://sms.nalosolutions.com",
        "https://api.nalosolutions.com/v1",
    ]

    paths = ["", "/sms", "/send", "/api/sms", "/v1/sms", "/sms/send"]

    print("🔍 Testing Nalo Solutions API endpoints...\n")

    for base_url in base_urls:
        for path in paths:
            full_url = base_url + path
            try:
                print(f"Testing: {full_url}")
                response = requests.get(full_url, timeout=5)
                print(f"  ✅ Status: {response.status_code}")
                if response.status_code == 200:
                    print(f"  📝 Content preview: {response.text[:100]}...")
                elif response.status_code in [301, 302]:
                    print(
                        f"  🔄 Redirect to: {response.headers.get('Location', 'Unknown')}"
                    )
                print()
            except requests.exceptions.RequestException as e:
                print(f"  ❌ Error: {str(e)}")
                print()


if __name__ == "__main__":
    test_endpoints()
