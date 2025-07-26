"""
Debug SMS test to see what's happening.
"""

from nunyakata.services.nalo_solutions import NaloSolutions


def test_sms_debug():
    """Debug SMS method."""
    config = {
        "sms": {
            "sender_id": "TEST_SENDER",
            "username": "test_user",
            "password": "test_pass",
            "auth_key": "test_auth_key",
        }
    }

    client = NaloSolutions(config)

    print(f"SMS Username: {client.sms_username}")
    print(f"SMS Password: {client.sms_password}")
    print(f"SMS Auth Key: {client.sms_auth_key}")
    print(f"SMS Sender ID: {client.sms_sender_id}")
    print(f"SMS Base URL: {client.sms_base_url}")

    # Try to mock the send_sms method to see what data it would send
    try:
        # This will fail because we don't have a mock, but we can catch it
        client.send_sms("233501234567", "Test message", "GET")
    except Exception as e:
        print(f"Error (expected): {e}")


if __name__ == "__main__":
    test_sms_debug()
