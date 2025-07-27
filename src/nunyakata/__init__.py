"""
Nunyakata - Ghana's Comprehensive API Integration Library

A unified Python library that simplifies integration with popular Ghanaian service APIs.
Currently supports Nalo Solutions for SMS, Email, USSD, and Payment services.

Example:
    from nunyakata import NaloSolutions, load_nalo_client_from_env

    # Option 1: Direct initialization
    client = NaloSolutions(
        payment_username="your_username",
        payment_password="your_password",
        merchant_id="your_merchant_id",
        sms_username="your_sms_username",
        sms_password="your_sms_password",
        sms_source="YourSource"
    )

    # Option 2: From environment variables
    client = load_nalo_client_from_env()

    # Send SMS
    response = client.send_sms("233501234567", "Hello from Nunyakata!")

    # Send Email
    email_response = client.send_email(
        recipient="user@example.com",
        sender="noreply@yoursite.com",
        subject="Welcome",
        message="Thank you for joining us!"
    )

    # Make Payment
    payment_response = client.make_payment(
        amount=100.00,
        phone_number="233501234567",
        wallet_type="mtn"
    )

    # Handle USSD
    ussd_response = client.handle_ussd_request({
        "sessionid": "12345",
        "msisdn": "233501234567",
        "userdata": "*123#"
    })
"""

__version__ = "0.1.1"
__author__ = "Joseph"
__email__ = "nunyakata@seveightech.com"

from .services.nalo_solutions import NaloSolutions
from .config import (
    load_nalo_client_from_env,
    get_env_config,
    validate_env_config,
    create_nalo_client,
)

__all__ = [
    "NaloSolutions",
    "load_nalo_client_from_env",
    "get_env_config",
    "validate_env_config",
    "create_nalo_client",
]
