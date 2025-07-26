"""
Comprehensive SMS API examples for Nalo Solutions.

This demonstrates all SMS functionality including GET/POST methods,
authentication options, and response handling.
"""

import os
from nunyakata import NaloSolutionsClient


def main():
    """Demonstrate SMS API usage with both authentication methods."""

    print("=== Nalo Solutions SMS API Demo ===\n")

    # === Method 1: Username/Password Authentication ===
    print("1. Using Username/Password Authentication")

    client_auth = NaloSolutionsClient(
        sms_username=os.getenv("NALO_SMS_USERNAME", "johndoe"),
        sms_password=os.getenv("NALO_SMS_PASSWORD", "password123"),
        sms_source=os.getenv("NALO_SMS_SOURCE", "NALO"),
    )

    try:
        # Send SMS using GET method (URL parameters)
        print("  a) Sending SMS via GET method...")
        response_get = client_auth.send_sms(
            recipient="233XXXXXXXXX",
            message="Test SMS via GET method from Nunyakata!",
            delivery_report=True,
            message_type="0",  # Text message
            use_post=False,
        )
        print(f"  GET Response: {response_get}")

        # Parse the response (only for GET method which returns string)
        if isinstance(response_get, str):
            parsed = client_auth.parse_sms_response(response_get)
            print(f"  Parsed: {parsed}")
            print(f"  Explanation: {client_auth.explain_sms_response(response_get)}")
        else:
            print(f"  POST response (JSON): {response_get}")

    except Exception as e:
        print(f"  Error with username/password auth: {e}")

    print("\n" + "=" * 60 + "\n")

    # === Method 2: Auth Key Authentication ===
    print("2. Using Auth Key Authentication")

    client_key = NaloSolutionsClient(
        sms_auth_key=os.getenv("NALO_SMS_AUTH_KEY", "your_auth_key_here"),
        sms_source=os.getenv("NALO_SMS_SOURCE", "NALO"),
    )

    try:
        # Send SMS using POST method (JSON)
        print("  a) Sending SMS via POST method...")
        response_post = client_key.send_sms(
            recipient="233XXXXXXXXX",
            message="Test SMS via POST method from Nunyakata!",
            use_post=True,
        )
        print(f"  POST Response: {response_post}")

    except Exception as e:
        print(f"  Error with auth key: {e}")

    print("\n" + "=" * 60 + "\n")

    # === Flash SMS Example ===
    print("3. Sending Flash SMS")

    try:
        flash_response = client_auth.send_flash_sms(
            recipient="233XXXXXXXXX",
            message="⚡ URGENT: This is a flash SMS that appears directly on screen!",
        )
        print(f"  Flash SMS Response: {flash_response}")

    except Exception as e:
        print(f"  Error with flash SMS: {e}")

    print("\n" + "=" * 60 + "\n")

    # === Bulk SMS Examples ===
    print("4. Bulk SMS Examples")

    recipients = ["233XXXXXXXXX", "233YYYYYYYYY", "233ZZZZZZZZZ"]

    try:
        # Method A: Individual requests for each recipient
        print("  a) Bulk SMS (individual requests)...")
        bulk_results = client_auth.send_bulk_sms(
            recipients=recipients,
            message="Bulk SMS test - individual requests",
            delivery_report=True,
            use_post=False,
        )
        print(f"  Individual Results: {bulk_results}")

    except Exception as e:
        print(f"  Error with individual bulk SMS: {e}")

    try:
        # Method B: Single request with comma-separated numbers
        print("  b) Bulk SMS (single request)...")
        single_bulk_result = client_key.send_bulk_sms_single_request(
            recipients=recipients,
            message="Bulk SMS test - single request with comma-separated numbers",
        )
        print(f"  Single Request Result: {single_bulk_result}")

    except Exception as e:
        print(f"  Error with single bulk SMS: {e}")

    print("\n" + "=" * 60 + "\n")

    # === Advanced Features ===
    print("5. Advanced SMS Features")

    try:
        # SMS with validity period and callback
        print("  a) SMS with validity period and callback...")
        advanced_response = client_auth.send_sms(
            recipient="233XXXXXXXXX",
            message="⏰ This SMS expires in 5 minutes!",
            delivery_report=True,
            validity_period=5,  # 5 minutes
            callback_url="https://yoursite.com/sms-callback",
            use_post=False,
        )
        print(f"  Advanced Response: {advanced_response}")

    except Exception as e:
        print(f"  Error with advanced SMS: {e}")

    print("\n" + "=" * 60 + "\n")

    # === Service Status Check ===
    print("6. Service Status Check")

    status = client_auth.get_service_status()
    print(f"  Service Status: {status}")

    print("\n" + "=" * 60 + "\n")

    # === Error Codes Reference ===
    print("7. SMS Error Codes Reference")

    error_codes = client_auth.get_sms_error_codes()
    print("  Available Error Codes:")
    for code, description in error_codes.items():
        print(f"    {code}: {description}")


def url_examples():
    """Show example URLs for different SMS methods."""

    print("\n" + "=" * 60)
    print("SMS API URL Examples (from official documentation)")
    print("=" * 60)

    print("\n1. GET with Username/Password:")
    print("https://sms.nalosolutions.com/smsbackend/clientapi/Resl_Nalo/send-message/")
    print("?username=johndoe&password=some_password&type=0&destination=233XXXXXXXXX")
    print("&dlr=1&source=NALO&message=This+is+a+test+from+Mars")

    print("\n2. GET with Auth Key:")
    print("https://sms.nalosolutions.com/smsbackend/clientapi/Resl_Nalo/send-message/")
    print("?key=YOUR_AUTH_KEY&type=0&destination=233XXXXXXXXX")
    print("&dlr=1&source=NALO&message=This+is+a+test+from+Mars")

    print("\n3. POST with Auth Key (JSON):")
    print("URL: https://sms.nalosolutions.com/smsbackend/Resl_Nalo/send-message/")
    print("Body: {")
    print('  "key": "your_auth_key",')
    print('  "msisdn": "233244071872, 233XXXXXXXX",')
    print('  "message": "Here are two, of many",')
    print('  "sender_id": "NALO"')
    print("}")

    print("\n4. POST with Username/Password (JSON):")
    print("URL: https://sms.nalosolutions.com/smsbackend/Resl_Nalo/send-message/")
    print("Body: {")
    print('  "username": "johndoe",')
    print('  "password": "password",')
    print('  "msisdn": "233XXXXXXXX",')
    print('  "message": "Here are two, of many",')
    print('  "sender_id": "Test"')
    print("}")


def test_response_parsing():
    """Test SMS response parsing with examples."""

    print("\n" + "=" * 60)
    print("SMS Response Parsing Examples")
    print("=" * 60)

    client = NaloSolutionsClient()

    # Test success response
    success_response = "1701|233501371674|api.0000011.20220418.0000001"
    parsed_success = client.parse_sms_response(success_response)
    print(f"\nSuccess Response: {success_response}")
    print(f"Parsed: {parsed_success}")
    print(f"Explanation: {client.explain_sms_response(success_response)}")

    # Test error responses
    error_responses = [
        "1702",  # Invalid URL Error
        "1703",  # Invalid username/password
        "1707",  # Invalid Source
        "1025",  # Insufficient Credit
    ]

    for error_response in error_responses:
        parsed_error = client.parse_sms_response(error_response)
        print(f"\nError Response: {error_response}")
        print(f"Parsed: {parsed_error}")
        print(f"Explanation: {client.explain_sms_response(error_response)}")


if __name__ == "__main__":
    # Run the main demo
    main()

    # Show URL examples
    url_examples()

    # Test response parsing
    test_response_parsing()

    print("\n" + "=" * 60)
    print("Environment Variables Setup")
    print("=" * 60)
    print("export NALO_SMS_USERNAME='your_username'")
    print("export NALO_SMS_PASSWORD='your_password'")
    print("export NALO_SMS_SOURCE='your_sender_id'")
    print(
        "export NALO_SMS_AUTH_KEY='your_auth_key'  # Alternative to username/password"
    )
    print("\nNote: You can use either username/password OR auth_key for authentication")
    print("=" * 60)
