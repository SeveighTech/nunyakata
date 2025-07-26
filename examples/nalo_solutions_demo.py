"""
Example usage of Nalo Solutions API integration.

This script de    # 4. Mobile Money Payment
    print("4. Processing mobile money payment...")
    try:
        payment_result = nalo_client.make_payment(
            order_id="myoder_15150",  # Your unique order ID
            key="1234",  # 4-digit random key for secret generation
            phone_number="233241000000",  # Must be 12 digits: 233xxxxxxxx
            item_desc="Test Product Purchase",
            amount="5.00",  # Amount as string in Ghanaian cedis
            network="MTN",  # Options: MTN, VODAFONE, AIRTELTIGO
            customer_name="Gideon",  # Customer/buyer name
            callback_url="https://yoursite.com/payment-callback"  # Optional
        )
        print(f"Payment Result: {payment_result}")
    except Exception as e:
        print(f"Error processing payment: {e}")

    print("\n" + "="*50 + "\n")

    # 4b. Vodafone Voucher Payment Example
    print("4b. Processing Vodafone voucher payment...")
    try:
        vodafone_payment = nalo_client.create_vodafone_voucher_payment(
            order_id="voda_order_123",
            key="5678",
            phone_number="233241000000",
            voucher_code="ABC123DEF",  # User-generated voucher code
            amount="10.00",
            customer_name="Test Customer"
        )
        print(f"Vodafone Voucher Payment: {vodafone_payment}")
    except Exception as e:
        print(f"Error with Vodafone voucher payment: {e}")

    print("\n" + "="*50 + "\n")

    # 4c. Vodafone USSD Payment Example
    print("4c. Processing Vodafone USSD payment...")
    try:
        vodafone_ussd = nalo_client.create_vodafone_ussd_payment(
            order_id="voda_ussd_456",
            key="9012",
            phone_number="233241000000",
            item_desc="Premium Service",
            amount="25.00",
            customer_name="Premium User"
        )
        print(f"Vodafone USSD Payment: {vodafone_ussd}")
    except Exception as e:
        print(f"Error with Vodafone USSD payment: {e}")o use all four Nalo Solutions services:
- Payments (Mobile Money)
- SMS
- USSD
- Email
"""

import os
from nunyakata import NaloSolutionsClient


def main():
    """Demonstrate Nalo Solutions API usage."""

    # Initialize client with credentials
    # You can set these as environment variables for security
    nalo_client = NaloSolutionsClient(
        # Payment API credentials
        payment_username=os.getenv("NALO_PAYMENT_USERNAME", "your_payment_username"),
        payment_password=os.getenv("NALO_PAYMENT_PASSWORD", "your_payment_password"),
        merchant_id=os.getenv("NALO_MERCHANT_ID", "your_merchant_id"),
        # SMS API credentials
        sms_username=os.getenv("NALO_SMS_USERNAME", "your_sms_username"),
        sms_password=os.getenv("NALO_SMS_PASSWORD", "your_sms_password"),
        sms_source=os.getenv("NALO_SMS_SOURCE", "your_sms_source"),
    )

    print("=== Nalo Solutions API Demo ===\n")

    # 1. Check service status
    print("1. Checking service status...")
    try:
        status = nalo_client.get_service_status()
        print(f"Service Status: {status}")
    except Exception as e:
        print(f"Error checking status: {e}")

    print("\n" + "=" * 50 + "\n")

    # 2. Send SMS
    print("2. Sending SMS...")
    try:
        sms_result = nalo_client.send_sms(
            recipient="233123456789",  # Replace with actual phone number
            message="Hello from Nunyakata! This is a test SMS via Nalo Solutions.",
        )
        print(f"SMS Result: {sms_result}")
    except Exception as e:
        print(f"Error sending SMS: {e}")

    print("\n" + "=" * 50 + "\n")

    # 3. Send Bulk SMS
    print("3. Sending bulk SMS...")
    try:
        recipients = ["233123456789", "233987654321"]  # Replace with actual numbers
        bulk_results = nalo_client.send_bulk_sms(
            recipients=recipients, message="Bulk SMS test from Nunyakata!"
        )
        print(f"Bulk SMS Results: {bulk_results}")
    except Exception as e:
        print(f"Error sending bulk SMS: {e}")

    print("\n" + "=" * 50 + "\n")

    # 4. Mobile Money Payment
    print("4. Processing mobile money payment...")
    try:
        payment_result = nalo_client.make_payment(
            order_id="ORDER12345",
            key="1234",  # Must be 4 digits
            phone_number="233241000000",  # Must be 12 digits
            item_desc="Test Product Payment",
            amount="10.00",  # Amount as string
            network="MTN",  # Options: MTN, VODAFONE, AIRTELTIGO
            customer_name="Test Customer",
            callback_url="https://yoursite.com/payment-callback",  # Optional
        )
        print(f"Payment Result: {payment_result}")
    except Exception as e:
        print(f"Error processing payment: {e}")

    print("\n" + "=" * 50 + "\n")

    # 5. Handle USSD Request (example)
    print("5. Handling USSD request...")
    try:
        # Example USSD request data (this would come from Nalo's USSD gateway)
        sample_ussd_data = {
            "USERID": "USER123",
            "MSISDN": "233123456789",
            "USERDATA": "",
            "MSGTYPE": True,  # True for new session, False for continuing
            "SESSIONID": "SESSION123",
            "NETWORK": "MTN",
        }

        ussd_response = nalo_client.handle_ussd_request(sample_ussd_data)
        print(f"USSD Response: {ussd_response}")
    except Exception as e:
        print(f"Error handling USSD: {e}")

    print("\n" + "=" * 50 + "\n")

    # 6. Send Email
    print("6. Sending email...")
    try:
        email_result = nalo_client.send_email(
            to_email="test@example.com",
            subject="Test Email from Nunyakata",
            message="This is a test email sent via Nalo Solutions API.",
            from_email="noreply@yoursite.com",
        )
        print(f"Email Result: {email_result}")
    except Exception as e:
        print(f"Error sending email: {e}")

    print("\n" + "=" * 50 + "\n")

    # 7. Check Account Balance
    print("7. Checking account balance...")
    try:
        balance = nalo_client.check_balance()
        print(f"Account Balance: {balance}")
    except Exception as e:
        print(f"Error checking balance: {e}")

    print("\n=== Demo Complete ===")


def flask_ussd_webhook_example():
    """
    Example Flask webhook for handling USSD requests from Nalo Solutions.
    This shows how you might integrate USSD handling in a web application.
    """
    from flask import Flask, request, jsonify

    app = Flask(__name__)

    # Initialize Nalo client
    nalo_client = NaloSolutionsClient(
        sms_username=os.getenv("NALO_SMS_USERNAME"),
        sms_password=os.getenv("NALO_SMS_PASSWORD"),
        sms_source=os.getenv("NALO_SMS_SOURCE"),
    )

    @app.route("/ussd-webhook", methods=["POST"])
    def handle_ussd_webhook():
        """Handle incoming USSD requests from Nalo Solutions."""
        try:
            # Get USSD data from request
            ussd_data = request.get_json()

            # Process USSD request using our client
            response = nalo_client.handle_ussd_request(ussd_data)

            # Return response to Nalo
            return jsonify(response)

        except Exception as e:
            # Error handling
            error_response = {
                "USERID": request.json.get("USERID", ""),
                "MSISDN": request.json.get("MSISDN", ""),
                "MSG": "Service temporarily unavailable. Please try again.",
                "MSGTYPE": False,
                "SESSIONID": request.json.get("SESSIONID", ""),
                "NETWORK": request.json.get("NETWORK", ""),
            }
            return jsonify(error_response)

    return app


def environment_setup_guide():
    """Print guide for setting up environment variables."""
    print(
        """
=== Environment Variables Setup Guide ===

To use Nalo Solutions API securely, set these environment variables:

# Payment API
export NALO_PAYMENT_USERNAME="your_payment_username"
export NALO_PAYMENT_PASSWORD="your_payment_password"
export NALO_MERCHANT_ID="your_merchant_id"

# SMS API
export NALO_SMS_USERNAME="your_sms_username"
export NALO_SMS_PASSWORD="your_sms_password"
export NALO_SMS_SOURCE="your_sms_source"

# Optional: Custom API URLs
export NALO_PAYMENT_URL="https://api.nalosolutions.com/payplus/api/"
export NALO_SMS_URL="https://sms.nalosolutions.com/smsbackend/clientapi/Resl_Nalo/send-message/"

=== Usage in Python ===

from nunyakata import NaloSolutionsClient
import os

# Initialize with environment variables
client = NaloSolutionsClient(
    payment_username=os.getenv("NALO_PAYMENT_USERNAME"),
    payment_password=os.getenv("NALO_PAYMENT_PASSWORD"),
    merchant_id=os.getenv("NALO_MERCHANT_ID"),
    sms_username=os.getenv("NALO_SMS_USERNAME"),
    sms_password=os.getenv("NALO_SMS_PASSWORD"),
    sms_source=os.getenv("NALO_SMS_SOURCE"),
)

# Now you can use all services
client.send_sms("233123456789", "Hello World!")
"""
    )


if __name__ == "__main__":
    # Uncomment the function you want to run

    # Basic demo
    main()

    # Environment setup guide
    # environment_setup_guide()

    # Flask webhook example (uncomment to create Flask app)
    # app = flask_ussd_webhook_example()
    # app.run(debug=True, port=5000)
