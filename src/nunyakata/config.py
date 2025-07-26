"""
Environment configuration utilities for Nunyakata.
"""

import os
from typing import Optional
from .services.nalo_solutions import NaloSolutionsClient


def load_nalo_client_from_env() -> NaloSolutionsClient:
    """
    Create a Nalo Solutions client using environment variables.

    Requires python-dotenv: pip install python-dotenv

    Environment variables expected:
    - NALO_PAYMENT_USERNAME, NALO_PAYMENT_PASSWORD, NALO_MERCHANT_ID (for payments)
    - NALO_SMS_USERNAME, NALO_SMS_PASSWORD, NALO_SMS_SOURCE (for SMS - method 1)
    - NALO_SMS_AUTH_KEY (for SMS - method 2, alternative to username/password)
    - NALO_EMAIL_USERNAME, NALO_EMAIL_PASSWORD (for email - method 1)
    - NALO_EMAIL_AUTH_KEY (for email - method 2, alternative to username/password)
    - NALO_PAYMENT_BASE_URL, NALO_SMS_BASE_URL, NALO_SMS_POST_URL, NALO_EMAIL_BASE_URL (optional)
    - NALO_API_KEY (optional)

    Returns:
        Configured NaloSolutionsClient instance

    Raises:
        ValueError: If required environment variables are missing

    Example:
        from nunyakata import load_nalo_client_from_env

        # Make sure to load environment variables first
        # from dotenv import load_dotenv
        # load_dotenv()

        client = load_nalo_client_from_env()

        # Use the client
        response = client.send_sms("233501234567", "Hello Ghana!")
        email_response = client.send_email("user@example.com", "sender@verified.com", "Subject", "Body", "Sender Name")
    """
    try:
        from dotenv import load_dotenv

        load_dotenv()
    except ImportError:
        # dotenv not installed, continue without it
        pass

    # Payment credentials
    payment_username = os.getenv("NALO_PAYMENT_USERNAME")
    payment_password = os.getenv("NALO_PAYMENT_PASSWORD")
    merchant_id = os.getenv("NALO_MERCHANT_ID")

    # SMS credentials - check for both auth methods
    sms_username = os.getenv("NALO_SMS_USERNAME")
    sms_password = os.getenv("NALO_SMS_PASSWORD")
    sms_source = os.getenv("NALO_SMS_SOURCE")
    sms_auth_key = os.getenv("NALO_SMS_AUTH_KEY")

    # Email credentials - check for both auth methods
    email_username = os.getenv("NALO_EMAIL_USERNAME")
    email_password = os.getenv("NALO_EMAIL_PASSWORD")
    email_auth_key = os.getenv("NALO_EMAIL_AUTH_KEY")

    # API endpoints (optional)
    payment_base_url = os.getenv("NALO_PAYMENT_BASE_URL")
    sms_base_url = os.getenv("NALO_SMS_BASE_URL")
    sms_post_url = os.getenv("NALO_SMS_POST_URL")
    email_base_url = os.getenv("NALO_EMAIL_BASE_URL")

    # General API key
    api_key = os.getenv("NALO_API_KEY")

    # Validate that we have at least some credentials
    has_payment_creds = payment_username and payment_password and merchant_id
    has_sms_creds = sms_auth_key or (sms_username and sms_password)
    has_email_creds = email_auth_key or (email_username and email_password)

    if not has_payment_creds and not has_sms_creds and not has_email_creds:
        raise ValueError(
            "No valid Nalo Solutions credentials found in environment variables. "
            "Please set payment credentials (NALO_PAYMENT_USERNAME, NALO_PAYMENT_PASSWORD, NALO_MERCHANT_ID) "
            "and/or SMS credentials (NALO_SMS_AUTH_KEY or NALO_SMS_USERNAME/NALO_SMS_PASSWORD) "
            "and/or email credentials (NALO_EMAIL_AUTH_KEY or NALO_EMAIL_USERNAME/NALO_EMAIL_PASSWORD)."
        )

    return NaloSolutionsClient(
        # Payment credentials
        payment_username=payment_username,
        payment_password=payment_password,
        merchant_id=merchant_id,
        # SMS credentials
        sms_username=sms_username,
        sms_password=sms_password,
        sms_source=sms_source,
        sms_auth_key=sms_auth_key,
        # Email credentials
        email_username=email_username,
        email_password=email_password,
        email_auth_key=email_auth_key,
        # API endpoints (will use defaults if None)
        payment_base_url=payment_base_url
        or "https://api.nalosolutions.com/payplus/api/",
        sms_base_url=sms_base_url
        or "https://sms.nalosolutions.com/smsbackend/clientapi/Resl_Nalo/send-message/",
        sms_post_url=sms_post_url
        or "https://sms.nalosolutions.com/smsbackend/Resl_Nalo/send-message/",
        email_base_url=email_base_url
        or "https://sms.nalosolutions.com/clientapi/Nal_resl/send-email/",
        # General API key
        api_key=api_key,
    )


def get_env_config() -> dict:
    """
    Get current environment configuration for Nunyakata.

    Returns:
        Dictionary containing configuration status and available services
    """
    try:
        from dotenv import load_dotenv

        load_dotenv()
    except ImportError:
        pass

    config = {
        "environment": os.getenv("ENVIRONMENT", "development"),
        "debug": os.getenv("DEBUG", "false").lower() == "true",
        "services": {
            "nalo_payments": bool(
                os.getenv("NALO_PAYMENT_USERNAME")
                and os.getenv("NALO_PAYMENT_PASSWORD")
                and os.getenv("NALO_MERCHANT_ID")
            ),
            "nalo_sms": bool(
                os.getenv("NALO_SMS_AUTH_KEY")
                or (os.getenv("NALO_SMS_USERNAME") and os.getenv("NALO_SMS_PASSWORD"))
            ),
        },
        "webhooks": {
            "payment_callback": os.getenv("PAYMENT_CALLBACK_URL"),
            "sms_delivery_callback": os.getenv("SMS_DELIVERY_CALLBACK_URL"),
            "ussd_callback": os.getenv("USSD_CALLBACK_URL"),
        },
        "testing": {
            "test_phone": os.getenv("TEST_PHONE_NUMBER"),
            "test_amount": os.getenv("TEST_PAYMENT_AMOUNT"),
        },
    }

    return config


def validate_env_config() -> tuple[bool, list[str]]:
    """
    Validate environment configuration.

    Returns:
        Tuple of (is_valid, list_of_missing_variables)
    """
    try:
        from dotenv import load_dotenv

        load_dotenv()
    except ImportError:
        pass

    missing = []

    # Check payment credentials
    payment_vars = [
        "NALO_PAYMENT_USERNAME",
        "NALO_PAYMENT_PASSWORD",
        "NALO_MERCHANT_ID",
    ]
    payment_missing = [var for var in payment_vars if not os.getenv(var)]

    # Check SMS credentials (either auth key OR username/password)
    sms_auth_key = os.getenv("NALO_SMS_AUTH_KEY")
    sms_user_pass = os.getenv("NALO_SMS_USERNAME") and os.getenv("NALO_SMS_PASSWORD")

    if not sms_auth_key and not sms_user_pass:
        missing.extend(
            ["NALO_SMS_AUTH_KEY or (NALO_SMS_USERNAME and NALO_SMS_PASSWORD)"]
        )

    # If we have some payment vars but not all, report missing ones
    if payment_missing and len(payment_missing) < len(payment_vars):
        missing.extend(payment_missing)

    is_valid = len(missing) == 0 and (
        len(payment_missing) == 0 or len(payment_missing) == len(payment_vars)
    )

    return is_valid, missing


# Convenience function for quick setup
def create_nalo_client(
    payment_username: Optional[str] = None,
    payment_password: Optional[str] = None,
    merchant_id: Optional[str] = None,
    sms_username: Optional[str] = None,
    sms_password: Optional[str] = None,
    sms_source: Optional[str] = None,
    sms_auth_key: Optional[str] = None,
    **kwargs,
) -> NaloSolutionsClient:
    """
    Create a Nalo Solutions client with explicit parameters or environment variables.

    If parameters are not provided, will try to load from environment variables.

    Args:
        payment_username: Payment API username
        payment_password: Payment API password
        merchant_id: Merchant ID for payments
        sms_username: SMS API username
        sms_password: SMS API password
        sms_source: SMS sender ID
        sms_auth_key: SMS auth key (alternative to username/password)
        **kwargs: Additional parameters passed to NaloSolutionsClient

    Returns:
        Configured NaloSolutionsClient instance
    """
    # If no explicit credentials provided, try environment variables
    if not any([payment_username, sms_username, sms_auth_key]):
        return load_nalo_client_from_env()

    return NaloSolutionsClient(
        payment_username=payment_username,
        payment_password=payment_password,
        merchant_id=merchant_id,
        sms_username=sms_username,
        sms_password=sms_password,
        sms_source=sms_source,
        sms_auth_key=sms_auth_key,
        **kwargs,
    )
