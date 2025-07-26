"""
Environment Configuration Example for Nunyakata

This example shows how to use environment variables to configure
the Nalo Solutions client for easy deployment and credential management.
"""

import os
from nunyakata import (
    load_nalo_client_from_env,
    get_env_config,
    validate_env_config,
    create_nalo_client,
)


def main():
    """Demonstrate environment-based configuration."""

    print("=== Nunyakata Environment Configuration Demo ===\n")

    # 1. Check current environment configuration
    print("1. Current Environment Configuration:")
    config = get_env_config()
    print(f"   Environment: {config['environment']}")
    print(f"   Debug Mode: {config['debug']}")
    print(f"   Nalo Payments Available: {config['services']['nalo_payments']}")
    print(f"   Nalo SMS Available: {config['services']['nalo_sms']}")
    print()

    # 2. Validate environment configuration
    print("2. Environment Validation:")
    is_valid, missing = validate_env_config()
    if is_valid:
        print("   ✅ Environment configuration is valid!")
    else:
        print("   ❌ Environment configuration has issues:")
        for var in missing:
            print(f"      - Missing: {var}")
    print()

    # 3. Try to create client from environment
    print("3. Creating Client from Environment:")
    try:
        client = load_nalo_client_from_env()
        print("   ✅ Client created successfully from environment variables!")

        # Check service status
        status = client.get_service_status()
        print(f"   SMS Auth Method: {status['sms_auth_method']}")
        print(f"   Available Services: {list(status['services'].keys())}")

        # Example SMS usage (if SMS credentials are available)
        if status["services"]["sms"]:
            print("\n   Attempting to send test SMS...")
            try:
                # Use test phone number from environment or default
                test_phone = os.getenv("TEST_PHONE_NUMBER", "233501234567")
                response = client.send_sms(
                    recipient=test_phone,
                    message="Test SMS from Nunyakata environment config!",
                )
                explanation = client.explain_sms_response(str(response))
                print(f"   SMS Response: {explanation}")
            except Exception as e:
                print(f"   SMS Test Failed: {e}")

        # Example payment usage (if payment credentials are available)
        if status["services"]["payments"]:
            print("\n   Payment service is available!")
            print("   (Skipping payment test to avoid charges)")

    except ValueError as e:
        print(f"   ❌ Failed to create client: {e}")
        print("\n   💡 Solution:")
        print("      1. Copy .env.example to .env")
        print("      2. Fill in your actual Nalo Solutions credentials")
        print("      3. Install python-dotenv: pip install python-dotenv")
    print()

    # 4. Alternative: Create client with explicit parameters
    print("4. Alternative: Creating Client with Explicit Parameters:")
    print("   (This would be useful for testing or when not using .env files)")
    print()
    print("   Example code:")
    print("   ```python")
    print("   client = create_nalo_client(")
    print("       sms_auth_key='your_auth_key_here',")
    print("       sms_source='YOUR_SENDER_ID',")
    print("       payment_username='your_username',")
    print("       payment_password='your_password',")
    print("       merchant_id='your_merchant_id'")
    print("   )")
    print("   ```")
    print()

    # 5. Environment variable examples
    print("5. Required Environment Variables:")
    print("   For SMS (choose one authentication method):")
    print("   - Method 1: NALO_SMS_USERNAME, NALO_SMS_PASSWORD, NALO_SMS_SOURCE")
    print("   - Method 2: NALO_SMS_AUTH_KEY, NALO_SMS_SOURCE")
    print()
    print("   For Payments:")
    print("   - NALO_PAYMENT_USERNAME, NALO_PAYMENT_PASSWORD, NALO_MERCHANT_ID")
    print()
    print("   Optional:")
    print("   - NALO_API_KEY, PAYMENT_CALLBACK_URL, SMS_DELIVERY_CALLBACK_URL")
    print()

    print("=== Demo Complete ===")


if __name__ == "__main__":
    main()
