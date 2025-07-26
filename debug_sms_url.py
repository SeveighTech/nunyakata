"""
Test to examine actual SMS URL generation.
"""

import requests_mock
from nunyakata.services.nalo_solutions import NaloSolutions


def test_sms_url_generation():
    """Test what URL is actually generated for SMS."""
    config = {
        "sms": {
            "sender_id": "TEST_SENDER",
            "username": "test_user",
            "password": "test_pass",
            "auth_key": None,  # Explicitly None
        }
    }

    client = NaloSolutions(config)

    with requests_mock.Mocker() as m:
        # Mock the expected URL
        m.get(requests_mock.ANY, json={"status": "success"})

        try:
            result = client.send_sms("233501234567", "Test message", "GET")
            print(f"Result: {result}")

            # Check what URL was actually called
            if m.request_history:
                actual_url = m.request_history[0].url
                print(f"Actual URL called: {actual_url}")
            else:
                print("No request was made")

        except Exception as e:
            print(f"Exception: {e}")


if __name__ == "__main__":
    test_sms_url_generation()
