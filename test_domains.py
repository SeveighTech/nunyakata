#!/usr/bin/env python3
"""
Test script to find the correct Nalo Solutions SMS API domain
"""

import requests
from urllib.parse import urlencode


def test_domains():
    """Test various possible domains for Nalo Solutions SMS API"""

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

    # Test different domain combinations
    domains = [
        "api.nalosolutions.com",
        "sms.nalosolutions.com",
        "nalosolutions.com",
        "www.nalosolutions.com",
        "gateway.nalosolutions.com",
        "msg.nalosolutions.com",
        "bulk.nalosolutions.com",
    ]

    paths = [
        "/clientapi/Resl_Nalo/send-message",
        "/sms/send-message",
        "/api/sms/send",
        "/send-message",
        "/sms/send",
        "/clientapi/send-message",
    ]

    print("🔍 Testing different domain and path combinations...\n")

    for domain in domains:
        print(f"Testing domain: {domain}")

        # First test if domain is reachable
        try:
            response = requests.get(f"https://{domain}", timeout=5)
            print(f"  ✅ Domain reachable - Status: {response.status_code}")

            # If domain is reachable, test SMS paths
            for path in paths:
                try:
                    url = f"https://{domain}{path}?" + urlencode(config)
                    response = requests.get(url, timeout=5)
                    print(f"    📱 {path} - Status: {response.status_code}")
                    if response.status_code not in [404, 500]:
                        print(f"       Response preview: {response.text[:100]}...")
                except requests.exceptions.RequestException as e:
                    print(f"    ❌ {path} - Error: {str(e)[:50]}...")

        except requests.exceptions.RequestException as e:
            print(f"  ❌ Domain unreachable: {str(e)[:60]}...")

        print()


if __name__ == "__main__":
    test_domains()
