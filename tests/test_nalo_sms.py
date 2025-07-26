"""
Tests for Nalo Solutions SMS API.
"""

import pytest
import requests
from urllib.parse import parse_qs, urlparse
from nunyakata.services.nalo_solutions import NaloSolutions


class TestNaloSMSAPI:
    """Test cases for Nalo SMS API functionality."""

    def test_send_sms_get_method_success(
        self, nalo_client, mock_requests, sms_success_response
    ):
        """Test successful SMS sending using GET method."""
        mock_requests.get(
            "https://api.nalosolutions.com/sms/", json=sms_success_response
        )

        result = nalo_client.send_sms(
            phone_number="233501234567", message="Test SMS message", method="GET"
        )

        assert result["status"] == "success"
        assert result["message_id"] == "msg_12345"

        # Verify GET request was made with correct parameters
        assert mock_requests.called
        request = mock_requests.request_history[0]
        assert request.method == "GET"

        # Parse query parameters
        parsed_url = urlparse(request.url)
        query_params = parse_qs(parsed_url.query)

        assert query_params["userid"][0] == "test_user"
        assert query_params["password"][0] == "test_pass"
        assert query_params["msg"][0] == "Test SMS message"
        assert query_params["sendid"][0] == "TEST_SENDER"
        assert query_params["phone"][0] == "233501234567"

    def test_send_sms_post_method_success(
        self, nalo_client, mock_requests, sms_success_response
    ):
        """Test successful SMS sending using POST method."""
        mock_requests.post(
            "https://api.nalosolutions.com/sms/", json=sms_success_response
        )

        result = nalo_client.send_sms(
            phone_number="233501234567", message="Test SMS message", method="POST"
        )

        assert result["status"] == "success"
        assert result["message_id"] == "msg_12345"

        # Verify POST request was made with correct data
        assert mock_requests.called
        request = mock_requests.request_history[0]
        assert request.method == "POST"

        # Check form data
        assert "userid=test_user" in request.text
        assert "password=test_pass" in request.text
        assert "msg=Test+SMS+message" in request.text
        assert "sendid=TEST_SENDER" in request.text
        assert "phone=233501234567" in request.text

    def test_send_sms_with_auth_key(
        self, nalo_client_with_auth_key, mock_requests, sms_success_response
    ):
        """Test SMS sending with auth key instead of username/password."""
        # Configure client to use auth key only
        client = nalo_client_with_auth_key
        # Remove username and password to force auth_key usage
        client.sms_username = None
        client.sms_password = None

        mock_requests.get(
            "https://api.nalosolutions.com/sms/", json=sms_success_response
        )

        result = client.send_sms(
            phone_number="233501234567", message="Test SMS with auth key", method="GET"
        )

        assert result["status"] == "success"

        # Verify auth key was used
        request = mock_requests.request_history[0]
        parsed_url = urlparse(request.url)
        query_params = parse_qs(parsed_url.query)

        assert query_params["authkey"][0] == "test_auth_key"
        assert "userid" not in query_params
        assert "password" not in query_params

    def test_send_sms_error(self, nalo_client, mock_requests, sms_error_response):
        """Test SMS sending with error response."""
        mock_requests.get(
            "https://api.nalosolutions.com/sms/",
            json=sms_error_response,
            status_code=400,
        )

        result = nalo_client.send_sms(
            phone_number="invalid_number", message="Test SMS message"
        )

        assert result["status"] == "error"
        assert "Invalid phone number" in result["message"]

    def test_send_sms_validation(self, nalo_client):
        """Test SMS parameter validation."""
        # Test missing phone number
        with pytest.raises(ValueError, match="Phone number must be provided"):
            nalo_client.send_sms(phone_number="", message="Test message")

        # Test missing message
        with pytest.raises(ValueError, match="Message must be provided"):
            nalo_client.send_sms(phone_number="233501234567", message="")

        # Test invalid method
        with pytest.raises(ValueError, match="Method must be 'GET' or 'POST'"):
            nalo_client.send_sms(
                phone_number="233501234567", message="Test message", method="PUT"
            )

    def test_send_sms_phone_number_formatting(
        self, nalo_client, mock_requests, sms_success_response
    ):
        """Test phone number formatting for SMS."""
        mock_requests.get(
            "https://api.nalosolutions.com/sms/", json=sms_success_response
        )

        # Test various phone number formats
        test_numbers = [
            "233501234567",  # Full format
            "0501234567",  # Local format
            "+233501234567",  # International format
        ]

        for phone_number in test_numbers:
            result = nalo_client.send_sms(
                phone_number=phone_number, message=f"Test message for {phone_number}"
            )
            assert result["status"] == "success"

    def test_send_sms_message_length_validation(self, nalo_client):
        """Test SMS message length validation."""
        # Test very long message (over 1000 characters)
        long_message = "A" * 1001

        with pytest.raises(ValueError, match="Message is too long"):
            nalo_client.send_sms(phone_number="233501234567", message=long_message)

    def test_send_sms_unicode_message(
        self, nalo_client, mock_requests, sms_success_response
    ):
        """Test SMS with unicode characters."""
        mock_requests.get(
            "https://api.nalosolutions.com/sms/", json=sms_success_response
        )

        unicode_message = "Hello! 🇬🇭 Welcome to Ghana. Akwaaba! ñáñá"

        result = nalo_client.send_sms(
            phone_number="233501234567", message=unicode_message
        )

        assert result["status"] == "success"

        # Verify unicode message was properly encoded in request
        request = mock_requests.request_history[0]
        parsed_url = urlparse(request.url)
        query_params = parse_qs(parsed_url.query)

        # The message should be URL encoded
        assert "msg" in query_params

    def test_send_bulk_sms(self, nalo_client, mock_requests, sms_success_response):
        """Test sending bulk SMS."""
        mock_requests.get(
            "https://api.nalosolutions.com/sms/", json=sms_success_response
        )

        phone_numbers = ["233501234567", "233509876543", "233507654321"]
        message = "Bulk SMS test message"

        results = []
        for phone_number in phone_numbers:
            result = nalo_client.send_sms(phone_number=phone_number, message=message)
            results.append(result)

        # All should be successful
        for result in results:
            assert result["status"] == "success"

        # Verify 3 requests were made
        assert len(mock_requests.request_history) == 3

    def test_send_sms_with_custom_sender_id(
        self, nalo_config, mock_requests, sms_success_response
    ):
        """Test SMS with custom sender ID."""
        mock_requests.get(
            "https://api.nalosolutions.com/sms/", json=sms_success_response
        )

        client = NaloSolutions(nalo_config)

        result = client.send_sms(
            phone_number="233501234567",
            message="Test with custom sender",
            sender_id="CUSTOM_ID",
        )

        assert result["status"] == "success"

        # Verify custom sender ID was used
        request = mock_requests.request_history[0]
        parsed_url = urlparse(request.url)
        query_params = parse_qs(parsed_url.query)

        assert query_params["sendid"][0] == "CUSTOM_ID"

    @pytest.mark.api
    def test_sms_api_timeout_handling(self, nalo_client, mock_requests):
        """Test handling of SMS API timeout."""
        mock_requests.get(
            "https://api.nalosolutions.com/sms/", exc=requests.exceptions.Timeout
        )

        result = nalo_client.send_sms(
            phone_number="233501234567", message="Timeout test message"
        )

        assert result["status"] == "error"
        assert "timeout" in result["message"].lower()

    @pytest.mark.api
    def test_sms_network_error_handling(self, nalo_client, mock_requests):
        """Test handling of SMS network errors."""
        mock_requests.get(
            "https://api.nalosolutions.com/sms/",
            exc=requests.exceptions.ConnectionError,
        )

        result = nalo_client.send_sms(
            phone_number="233501234567", message="Network error test message"
        )

        assert result["status"] == "error"
        assert (
            "network" in result["message"].lower()
            or "connection" in result["message"].lower()
        )

    def test_sms_rate_limiting_simulation(self, nalo_client, mock_requests):
        """Test handling of rate limiting (HTTP 429)."""
        mock_requests.get(
            "https://api.nalosolutions.com/sms/",
            status_code=429,
            json={"status": "error", "message": "Rate limit exceeded"},
        )

        result = nalo_client.send_sms(
            phone_number="233501234567", message="Rate limit test message"
        )

        assert result["status"] == "error"
        assert (
            "rate limit" in result["message"].lower()
            or "too many" in result["message"].lower()
        )

    def test_sms_no_authentication_error(self, nalo_config):
        """Test SMS sending without authentication credentials."""
        # Remove all authentication
        nalo_config["sms"]["username"] = None
        nalo_config["sms"]["password"] = None
        nalo_config["sms"]["auth_key"] = None

        client = NaloSolutions(nalo_config)

        with pytest.raises(
            ValueError, match="Authentication credentials must be provided"
        ):
            client.send_sms(phone_number="233501234567", message="Test message")
