"""Tests for Nalo Email API functionality - Fixed to match actual implementation."""

import pytest
import requests
from unittest.mock import mock_open, patch
from nunyakata.services.nalo_solutions import NaloSolutions


class TestNaloEmailAPI:
    """Test suite for Nalo Email API."""

    @pytest.fixture
    def nalo_config(self):
        """Configuration for Nalo client with email credentials."""
        return {
            "email": {
                "username": "test_user",
                "password": "test_password",
                "from_email": "test@example.com",
                "from_name": "Test Sender",
            }
        }

    @pytest.fixture
    def nalo_client_with_auth_key(self):
        """Create Nalo client instance with auth key."""
        config = {
            "email": {
                "auth_key": "test_auth_key",
                "from_email": "test@example.com",
                "from_name": "Test Sender",
                "username": None,
                "password": None,
            }
        }
        return NaloSolutions(config)

    @pytest.fixture
    def nalo_client(self, nalo_config):
        """Create Nalo client instance."""
        return NaloSolutions(nalo_config)

    @pytest.fixture
    def email_success_response(self):
        """Mock successful email response."""
        return {
            "status": "success",
            "message": "Email sent successfully",
            "message_id": "email_12345",
        }

    @pytest.fixture
    def email_error_response(self):
        """Mock email error response."""
        return {
            "status": "error",
            "message": "Invalid email address",
            "code": "INVALID_EMAIL",
        }

    @pytest.fixture
    def bulk_email_recipients(self):
        """Mock bulk email recipients."""
        return ["user1@example.com", "user2@example.com", "user3@example.com"]

    @pytest.fixture
    def sample_html_content(self):
        """Sample HTML content for testing."""
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

    def test_send_email_success(
        self, nalo_client, mock_requests, email_success_response
    ):
        """Test successful email sending."""
        mock_requests.post(
            "https://sms.nalosolutions.com/smsbackend/clientapi/Nal_resl/send-email/",
            json=email_success_response,
        )

        result = nalo_client.send_email(
            to_email="recipient@example.com",
            subject="Test Email",
            message="This is a test email message",
        )

        assert result["status"] == "success"
        assert result["message"] == "Email sent successfully"

    def test_send_email_with_auth_key(
        self, nalo_client_with_auth_key, mock_requests, email_success_response
    ):
        """Test email sending with auth key instead of username/password."""
        client = nalo_client_with_auth_key

        mock_requests.post(
            "https://sms.nalosolutions.com/smsbackend/clientapi/Nal_resl/send-email/",
            json=email_success_response,
        )

        result = client.send_email(
            to_email="recipient@example.com",
            subject="Test Email with Auth Key",
            message="Test message",
        )

        assert result["status"] == "success"

    def test_send_html_email(
        self, nalo_client, mock_requests, email_success_response, sample_html_content
    ):
        """Test sending HTML email."""
        mock_requests.post(
            "https://sms.nalosolutions.com/smsbackend/clientapi/Nal_resl/send-email/",
            json=email_success_response,
        )

        result = nalo_client.send_html_email(
            to_email="recipient@example.com",
            subject="HTML Test Email",
            html_content=sample_html_content,
        )

        assert result["status"] == "success"

    def test_send_bulk_email(
        self, nalo_client, mock_requests, email_success_response, bulk_email_recipients
    ):
        """Test sending bulk emails."""
        mock_requests.post(
            "https://sms.nalosolutions.com/smsbackend/clientapi/Nal_resl/send-email/",
            json=email_success_response,
        )

        result = nalo_client.send_bulk_email(
            recipients=bulk_email_recipients,
            subject="Bulk Email Test",
            message="This is a bulk email message",
        )

        assert result["status"] == "success"

    def test_send_email_with_template(
        self, nalo_client, mock_requests, email_success_response
    ):
        """Test sending email with template."""
        mock_requests.post(
            "https://sms.nalosolutions.com/smsbackend/clientapi/Nal_resl/send-email/",
            json=email_success_response,
        )

        result = nalo_client.send_email_with_template(
            to_email="john@example.com",
            template_name="welcome_template",
            content="Welcome to our service!",
            subject="Welcome John!",
        )

        assert result["status"] == "success"

    def test_send_email_with_attachment(
        self, nalo_client, mock_requests, email_success_response
    ):
        """Test sending email with file attachment."""
        mock_requests.post(
            "https://sms.nalosolutions.com/smsbackend/clientapi/Nal_resl/send-email/",
            json=email_success_response,
        )

        # Mock file content
        file_content = "Test file content"
        with patch("builtins.open", mock_open(read_data=file_content)):
            result = nalo_client.send_email(
                to_email="recipient@example.com",
                subject="Email with Attachment",
                message="Please find attached file.",
                attachments=["test_file.txt"],
            )

        assert result["status"] == "success"

    def test_send_email_error(self, nalo_client, mock_requests, email_error_response):
        """Test email sending with error response."""
        mock_requests.post(
            "https://sms.nalosolutions.com/smsbackend/clientapi/Nal_resl/send-email/",
            json=email_error_response,
            status_code=400,
        )

        result = nalo_client.send_email(
            to_email="user@invalid-domain.com",
            subject="Test Email",
            message="Test message",
        )

        assert result["status"] == "error"
        assert "Invalid email address" in result["message"]

    def test_email_validation(self, nalo_client):
        """Test email parameter validation."""
        # Test missing to_email
        with pytest.raises(ValueError, match="To email must be provided"):
            nalo_client.send_email(to_email="", subject="Test", message="Test")

        # Test missing subject
        with pytest.raises(ValueError, match="Subject must be provided"):
            nalo_client.send_email(
                to_email="test@example.com", subject="", message="Test"
            )

        # Test missing message
        with pytest.raises(ValueError, match="Message must be provided"):
            nalo_client.send_email(
                to_email="test@example.com", subject="Test", message=""
            )

    def test_email_address_validation(self, nalo_client):
        """Test email address validation."""
        # Test invalid email format
        with pytest.raises(ValueError, match="Invalid email address format"):
            nalo_client.send_email(
                to_email="invalid-email", subject="Test", message="Test"
            )

        # Test email list with invalid address
        with pytest.raises(ValueError, match="Invalid email address format"):
            nalo_client.send_email(
                to_email=["valid@example.com", "invalid-email"],
                subject="Test",
                message="Test",
            )

    def test_handle_email_callback(self, nalo_client):
        """Test email callback handling."""
        # Simulate callback data
        callback_data = {
            "mid": "email_12345",
            "status_desc": "delivered",
            "destination_address": "test@example.com",
            "sender_address": "sender@example.com",
            "timestamp": "2024-01-01T10:00:00Z",
        }

        result = nalo_client.handle_email_callback(callback_data)

        assert result["processed"] is True
        assert result["email_id"] == "email_12345"
        assert result["status"] == "delivered"

    def test_email_callback_error_handling(self, nalo_client):
        """Test email callback with invalid data."""
        # Missing required fields
        callback_data = {
            "timestamp": "2024-01-01T10:00:00Z",
        }

        result = nalo_client.handle_email_callback(callback_data)

        assert result["processed"] is False
        assert "Invalid callback data" in result["error"]

    def test_email_content_encoding(
        self, nalo_client, mock_requests, email_success_response
    ):
        """Test email with unicode content."""
        mock_requests.post(
            "https://sms.nalosolutions.com/smsbackend/clientapi/Nal_resl/send-email/",
            json=email_success_response,
        )

        unicode_content = "Hello! 🇬🇭 Welcome to Ghana. Akwaaba! ñáñá"

        result = nalo_client.send_email(
            to_email="recipient@example.com",
            subject="Unicode Test Email",
            message=unicode_content,
        )

        assert result["status"] == "success"

    @pytest.mark.api
    def test_email_api_timeout_handling(self, nalo_client, mock_requests):
        """Test handling of email API timeout."""
        mock_requests.post(
            "https://sms.nalosolutions.com/smsbackend/clientapi/Nal_resl/send-email/",
            exc=requests.exceptions.Timeout,
        )

        result = nalo_client.send_email(
            to_email="recipient@example.com",
            subject="Timeout Test",
            message="Test message",
        )

        assert result["status"] == "error"
        assert "timeout" in result["message"].lower()

    @pytest.mark.api
    def test_email_network_error_handling(self, nalo_client, mock_requests):
        """Test handling of email network errors."""
        mock_requests.post(
            "https://sms.nalosolutions.com/smsbackend/clientapi/Nal_resl/send-email/",
            exc=requests.exceptions.ConnectionError,
        )

        result = nalo_client.send_email(
            to_email="recipient@example.com",
            subject="Network Error Test",
            message="Test message",
        )

        assert result["status"] == "error"
        assert (
            "network" in result["message"].lower()
            or "connection" in result["message"].lower()
        )

    def test_email_no_authentication_error(self, nalo_config):
        """Test email without authentication credentials."""
        # Remove authentication
        nalo_config["email"]["username"] = None
        nalo_config["email"]["password"] = None
        nalo_config["email"]["auth_key"] = None

        client = NaloSolutions(nalo_config)

        with pytest.raises(
            ValueError, match="Authentication credentials must be provided"
        ):
            client.send_email(
                to_email="test@example.com", subject="Test", message="Test message"
            )
