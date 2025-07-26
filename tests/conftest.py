"""
Pytest configura        "sms": {
            "sender_id": "TEST_SENDER",
            "username": "test_user",
            "password": "test_pass",
            "auth_key": None  # Set to None so username/password takes precedence
        },nd fixtures for nunyakata tests.
"""

import pytest
import requests_mock

from nunyakata.client import NunyakataClient
from nunyakata.services.nalo_solutions import NaloSolutions


@pytest.fixture
def nalo_config():
    """Basic Nalo Solutions configuration for testing."""
    return {
        "payment": {
            "public_key": "test_public_key",
            "private_key": "test_private_key",
            "environment": "sandbox",
        },
        "sms": {
            "sender_id": "TEST_SENDER",
            "username": "test_user",
            "password": "test_pass",
            "auth_key": "test_auth_key",
        },
        "ussd": {
            "userid": "test_userid",
            "msisdn": "233501234567",
            "environment": "sandbox",
        },
        "email": {
            "username": "test_user",
            "password": "test_pass",
            "auth_key": "test_auth_key",
            "from_email": "test@example.com",
            "from_name": "Test Sender",
        },
    }


@pytest.fixture
def nalo_client(nalo_config):
    """NaloSolutions client instance with test configuration."""
    # Remove auth_key for basic tests so username/password takes precedence
    config = nalo_config.copy()
    config["sms"] = config["sms"].copy()
    config["email"] = config["email"].copy()
    del config["sms"]["auth_key"]
    del config["email"]["auth_key"]
    return NaloSolutions(config)


@pytest.fixture
def nalo_client_with_auth_key(nalo_config):
    """NaloSolutions client instance with auth_key configuration."""
    return NaloSolutions(nalo_config)


@pytest.fixture
def nunyakata_client():
    """Main NunyakataClient instance for testing."""
    return NunyakataClient()


@pytest.fixture
def mock_requests():
    """Requests mock fixture for HTTP mocking."""
    with requests_mock.Mocker() as m:
        yield m


@pytest.fixture
def payment_success_response():
    """Mock successful payment response."""
    return {
        "status": "success",
        "transaction_id": "txn_12345",
        "reference": "REF123",
        "amount": 10.00,
        "message": "Payment successful",
    }


@pytest.fixture
def payment_error_response():
    """Mock payment error response."""
    return {
        "status": "error",
        "message": "Insufficient funds",
        "code": "INSUFFICIENT_FUNDS",
    }


@pytest.fixture
def sms_success_response():
    """Mock successful SMS response."""
    return {
        "status": "success",
        "message": "SMS sent successfully",
        "message_id": "msg_12345",
        "credits_used": 1,
    }


@pytest.fixture
def sms_error_response():
    """Mock SMS error response."""
    return {
        "status": "error",
        "message": "Invalid phone number",
        "code": "INVALID_PHONE",
    }


@pytest.fixture
def ussd_session_data():
    """Mock USSD session data."""
    return {
        "sessionid": "sess_12345",
        "msisdn": "233501234567",
        "userid": "test_userid",
        "msg": "Welcome to test service",
        "msgtype": True,
    }


@pytest.fixture
def email_success_response():
    """Mock successful email response."""
    return {
        "status": "success",
        "message": "Email sent successfully",
        "message_id": "email_12345",
    }


@pytest.fixture
def email_error_response():
    """Mock email error response."""
    return {
        "status": "error",
        "message": "Invalid email address",
        "code": "INVALID_EMAIL",
    }


@pytest.fixture
def sample_html_content():
    """Sample HTML content for email testing."""
    return """
    <html>
    <body>
        <h1>Test Email</h1>
        <p>This is a test email with <strong>HTML content</strong>.</p>
        <ul>
            <li>Item 1</li>
            <li>Item 2</li>
        </ul>
    </body>
    </html>
    """


@pytest.fixture
def sample_email_template():
    """Sample email template for testing."""
    return {
        "subject": "Welcome {{name}}!",
        "body": "Hello {{name}}, welcome to {{service}}!",
        "html_body": "<h1>Welcome {{name}}!</h1><p>Hello {{name}}, welcome to {{service}}!</p>",
    }


@pytest.fixture
def bulk_email_recipients():
    """Sample bulk email recipients."""
    return [
        {"email": "user1@example.com", "name": "User One"},
        {"email": "user2@example.com", "name": "User Two"},
        {"email": "user3@example.com", "name": "User Three"},
    ]
