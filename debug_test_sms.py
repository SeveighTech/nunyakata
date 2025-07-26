#!/usr/bin/env python3
"""
Debug the actual SMS test request to see what URL is being generated.
"""

import requests_mock
from urllib.parse import parse_qs, urlparse
from nunyakata.services.nalo_solutions import NaloSolutions

# Create the config exactly like in conftest.py
sms_config = {
    "username": "test_user",
    "password": "test_pass",
    "sender_id": "TEST_SENDER",
}

config = {"sms": sms_config}
nalo_client = NaloSolutions(config)

# Mock the response
with requests_mock.Mocker() as m:
    sms_success_response = {
        "status": "success",
        "message": "SMS sent successfully",
        "message_id": "msg_12345",
        "credits_used": 1,
    }

    m.get("https://api.nalosolutions.com/sms/", json=sms_success_response)

    # Call send_sms exactly like in the test
    result = nalo_client.send_sms(
        phone_number="233501234567", message="Test SMS message", method="GET"
    )

    print("Result:", result)
    print("Mock called:", m.called)

    if m.called:
        request = m.request_history[0]
        print("Request method:", request.method)
        print("Request URL:", request.url)

        # Parse query parameters
        parsed_url = urlparse(request.url)
        query_params = parse_qs(parsed_url.query)
        print("Query parameters:", query_params)

        # Check for expected parameters
        expected_params = ["userid", "password", "msg", "sendid", "phone"]
        for param in expected_params:
            if param in query_params:
                print(f"✓ {param}: {query_params[param][0]}")
            else:
                print(f"✗ {param}: NOT FOUND")

        # Show all available parameters
        print("\nAll available parameters:")
        for key, value in query_params.items():
            print(f"  {key}: {value[0]}")
