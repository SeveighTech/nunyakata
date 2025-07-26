"""
Tests for Nalo Solutions Email API.
"""

import pytest
import requests
from unittest.mock import patch, mock_open
from nunyakata.services.nalo_solutions import NaloSolutions


class TestNaloEmailAPI:
    """Test cases for Nalo Email API functionality."""

    def test_send_email_json_success(
        self, nalo_client, mock_requests, email_success_response
    ):
        """Test successful email sending using JSON format."""
        mock_requests.post(
            "https://api.nalosolutions.com/sendemail/", json=email_success_response
        )

        result = nalo_client.send_email(
            to_email="recipient@example.com",
            subject="Test Email",
            message="This is a test email message",
            send_format="json",
        )

        assert result["status"] == "success"
        assert result["message_id"] == "email_12345"

        # Verify JSON request was made correctly
        assert mock_requests.called
        request = mock_requests.request_history[0]
        assert request.method == "POST"
        assert request.headers["Content-Type"] == "application/json"

        request_data = request.json()
        assert request_data["to"] == "recipient@example.com"
        assert request_data["subject"] == "Test Email"
        assert request_data["message"] == "This is a test email message"
        assert request_data["username"] == "test_user"
        assert request_data["password"] == "test_pass"

    def test_send_email_form_data_success(
        self, nalo_client, mock_requests, email_success_response
    ):
        """Test successful email sending using form data format."""
        mock_requests.post(
            "https://api.nalosolutions.com/sendemail/", json=email_success_response
        )

        result = nalo_client.send_email(
            to_email="recipient@example.com",
            subject="Test Email",
            message="This is a test email message",
            send_format="form",
        )

        assert result["status"] == "success"
        assert result["message_id"] == "email_12345"

        # Verify form data request was made correctly
        assert mock_requests.called
        request = mock_requests.request_history[0]
        assert request.method == "POST"
        assert "multipart/form-data" in request.headers["Content-Type"]

    def test_send_email_with_auth_key(
        self, nalo_config, mock_requests, email_success_response
    ):
        """Test email sending with auth key instead of username/password."""
        # Configure client to use auth key
        nalo_config["email"]["username"] = None
        nalo_config["email"]["password"] = None
        client = NaloSolutions(nalo_config)

        mock_requests.post(
            "https://api.nalosolutions.com/sendemail/", json=email_success_response
        )

        result = client.send_email(
            to_email="recipient@example.com",
            subject="Test Email with Auth Key",
            message="Test message",
            send_format="json",
        )

        assert result["status"] == "success"

        # Verify auth key was used
        request = mock_requests.request_history[0]
        request_data = request.json()
        assert request_data["authkey"] == "test_auth_key"
        assert "username" not in request_data
        assert "password" not in request_data

    def test_send_html_email(
        self, nalo_client, mock_requests, email_success_response, sample_html_content
    ):
        """Test sending HTML email."""
        mock_requests.post(
            "https://api.nalosolutions.com/sendemail/", json=email_success_response
        )

        result = nalo_client.send_html_email(
            to_email="recipient@example.com",
            subject="HTML Test Email",
            html_content=sample_html_content,
        )

        assert result["status"] == "success"

        # Verify HTML content was sent
        request = mock_requests.request_history[0]
        request_data = request.json()
        assert request_data["message"] == sample_html_content
        assert request_data["content_type"] == "html"

    def test_send_bulk_email(
        self, nalo_client, mock_requests, email_success_response, bulk_email_recipients
    ):
        """Test sending bulk emails."""
        mock_requests.post(
            "https://api.nalosolutions.com/sendemail/", json=email_success_response
        )

        result = nalo_client.send_bulk_email(
            recipients=bulk_email_recipients,
            subject="Bulk Email Test",
            message="This is a bulk email message",
        )

        assert result["status"] == "success"

        # Verify bulk email request
        assert len(mock_requests.request_history) == len(bulk_email_recipients)

        # Check each request
        for i, request in enumerate(mock_requests.request_history):
            request_data = request.json()
            assert request_data["to"] == bulk_email_recipients[i]["email"]
            assert request_data["subject"] == "Bulk Email Test"

    def test_send_email_with_template(
        self, nalo_client, mock_requests, email_success_response, sample_email_template
    ):
        """Test sending email with template."""
        mock_requests.post(
            "https://api.nalosolutions.com/sendemail/", json=email_success_response
        )

        template_data = {"name": "John Doe", "service": "Test Service"}

        result = nalo_client.send_email_with_template(
            to_email="john@example.com",
            template=sample_email_template,
            template_data=template_data,
        )

        assert result["status"] == "success"

        # Verify template was processed
        request = mock_requests.request_history[0]
        request_data = request.json()
        assert request_data["subject"] == "Welcome John Doe!"
        assert "Hello John Doe, welcome to Test Service!" in request_data["message"]

    def test_send_email_with_attachment(
        self, nalo_client, mock_requests, email_success_response
    ):
        """Test sending email with file attachment."""
        mock_requests.post(
            "https://api.nalosolutions.com/sendemail/", json=email_success_response
        )

        # Mock file content
        file_content = "Test file content"
        with patch("builtins.open", mock_open(read_data=file_content)):
            result = nalo_client.send_email(
                to_email="recipient@example.com",
                subject="Email with Attachment",
                message="Please find attached file.",
                attachments=["test_file.txt"],
                send_format="form",
            )

        assert result["status"] == "success"

        # Verify attachment was included
        request = mock_requests.request_history[0]
        assert "multipart/form-data" in request.headers["Content-Type"]

    def test_send_email_error(self, nalo_client, mock_requests, email_error_response):
        """Test email sending with error response."""
        mock_requests.post(
            "https://api.nalosolutions.com/sendemail/",
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
        # Test missing required parameters
        with pytest.raises(ValueError, match="To email must be provided"):
            nalo_client.send_email(to_email="", subject="Test", message="Test")

        with pytest.raises(ValueError, match="Subject must be provided"):
            nalo_client.send_email(
                to_email="test@example.com", subject="", message="Test"
            )

        with pytest.raises(ValueError, match="Message must be provided"):
            nalo_client.send_email(
                to_email="test@example.com", subject="Test", message=""
            )

    def test_email_address_validation(self, nalo_client):
        """Test email address format validation."""
        # Valid email addresses
        valid_emails = [
            "user@example.com",
            "test.user@domain.co.uk",
            "user+tag@example.org",
        ]

        for email in valid_emails:
            assert nalo_client.validate_email(email)

        # Invalid email addresses
        invalid_emails = [
            "invalid-email",
            "@example.com",
            "user@",
            "user space@example.com",
            "",
        ]

        for email in invalid_emails:
            assert not nalo_client.validate_email(email)

    def test_handle_email_callback(self, nalo_client):
        """Test email callback handling."""
        # Simulate callback data
        callback_data = {
            "message_id": "email_12345",
            "status": "delivered",
            "recipient": "test@example.com",
            "timestamp": "2024-01-01T10:00:00Z",
        }

        result = nalo_client.handle_email_callback(callback_data)

        assert result["processed"] is True
        assert result["message_id"] == "email_12345"
        assert result["status"] == "delivered"

    def test_email_callback_error_handling(self, nalo_client):
        """Test email callback error handling."""
        # Invalid callback data
        invalid_callback_data = {"invalid": "data"}

        result = nalo_client.handle_email_callback(invalid_callback_data)

        assert result["processed"] is False
        assert "error" in result

    def test_email_with_custom_headers(
        self, nalo_client, mock_requests, email_success_response
    ):
        """Test sending email with custom headers."""
        mock_requests.post(
            "https://api.nalosolutions.com/sendemail/", json=email_success_response
        )

        custom_headers = {"Reply-To": "noreply@example.com", "X-Priority": "1"}

        result = nalo_client.send_email(
            to_email="recipient@example.com",
            subject="Email with Custom Headers",
            message="Test message",
            custom_headers=custom_headers,
        )

        assert result["status"] == "success"

        # Verify custom headers were included
        request = mock_requests.request_history[0]
        request_data = request.json()
        assert "custom_headers" in request_data
        assert request_data["custom_headers"]["Reply-To"] == "noreply@example.com"

    def test_email_content_encoding(
        self, nalo_client, mock_requests, email_success_response
    ):
        """Test email with unicode content."""
        mock_requests.post(
            "https://api.nalosolutions.com/sendemail/", json=email_success_response
        )

        unicode_content = "Hello! 🇬🇭 Welcome to Ghana. Akwaaba! ñáñá"

        result = nalo_client.send_email(
            to_email="recipient@example.com",
            subject="Unicode Test Email",
            message=unicode_content,
        )

        assert result["status"] == "success"

        # Verify unicode content was properly handled
        request = mock_requests.request_history[0]
        request_data = request.json()
        assert request_data["message"] == unicode_content

    @pytest.mark.api
    def test_email_api_timeout_handling(self, nalo_client, mock_requests):
        """Test handling of email API timeout."""
        mock_requests.post(
            "https://api.nalosolutions.com/sendemail/", exc=requests.exceptions.Timeout
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
            "https://api.nalosolutions.com/sendemail/",
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

    def test_email_rate_limiting(self, nalo_client, mock_requests):
        """Test handling of email rate limiting."""
        mock_requests.post(
            "https://api.nalosolutions.com/sendemail/",
            status_code=429,
            json={"status": "error", "message": "Rate limit exceeded"},
        )

        result = nalo_client.send_email(
            to_email="recipient@example.com",
            subject="Rate Limit Test",
            message="Test message",
        )

        assert result["status"] == "error"
        assert (
            "rate limit" in result["message"].lower()
            or "too many" in result["message"].lower()
        )

    def test_email_no_authentication_error(self, nalo_config):
        """Test email sending without authentication credentials."""
        # Remove all authentication
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
