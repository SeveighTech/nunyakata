"""Tests for Nalo SMS API functionality - Fixed to match actual implementation."""

import pytest
import requests
from nunyakata.services.nalo_solutions import NaloSolutions


class TestNaloSMSAPI:
    """Test suite for Nalo SMS API."""

    @pytest.fixture
    def nalo_config(self):
        """Configuration for Nalo client with SMS credentials."""
        return {
            "sms": {
                "username": "test_user",
                "password": "test_pass",
                "sender_id": "TEST_SENDER",
            }
        }

    @pytest.fixture
    def nalo_client_with_auth_key(self):
        """Create Nalo client instance with auth key."""
        config = {
            "sms": {
                "auth_key": "test_auth_key_12345",
                "sender_id": "TEST_SENDER",
            }
        }
        return NaloSolutions(config)

    @pytest.fixture
    def nalo_client(self, nalo_config):
        """Create Nalo client instance."""
        return NaloSolutions(nalo_config)

    @pytest.fixture
    def sms_success_response(self):
        """Mock successful SMS response."""
        return {
            "status": "success",
            "message": "SMS sent successfully",
            "message_id": "msg_12345",
            "credits_used": 1,
        }

    @pytest.fixture
    def sms_error_response(self):
        """Mock SMS error response."""
        return {
            "status": "error",
            "message": "Invalid phone number",
            "code": "INVALID_PHONE",
        }

    def test_send_sms_get_method_success(
        self, nalo_client, mock_requests, sms_success_response
    ):
        """Test successful SMS sending using GET method."""
        # Mock the raw response format for GET method
        mock_requests.get(
            "https://sms.nalosolutions.com/smsbackend/clientapi/Resl_Nalo/send-message",
            text="1701|233501234567|api.0039013.20250127.1753576627.8301058",
        )

        result = nalo_client.send_sms(
            phone_number="233501234567", message="Test SMS message", method="GET"
        )

        assert result["status"] == "success"
        assert result["message"] == "SMS sent successfully"
        assert "message_id" in result

    def test_send_sms_post_method_success(
        self, nalo_client, mock_requests, sms_success_response
    ):
        """Test successful SMS sending using POST method."""
        # Mock the JSON response format for POST method
        mock_requests.post(
            "https://sms.nalosolutions.com/smsbackend/Resl_Nalo/send-message/",
            text='{"status": "1701", "job_id": "api.0000011.20221222.0000003", "msisdn": "233244071872"}',
        )

        result = nalo_client.send_sms(
            phone_number="233501234567", message="Test SMS message", method="POST"
        )

        assert result["status"] == "success"
        assert result["message"] == "SMS sent successfully"
        assert "message_id" in result

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
            "https://sms.nalosolutions.com/smsbackend/clientapi/Resl_Nalo/send-message",
            text="1701|233501234567|api.0039013.20250127.1753576627.8301058",
        )

        result = client.send_sms(
            phone_number="233501234567", message="Test SMS with auth key", method="GET"
        )

        assert result["status"] == "success"

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
                phone_number="233501234567", message="Test", method="INVALID"
            )

    def test_send_sms_message_length_validation(self, nalo_client):
        """Test SMS message length validation."""
        # Test message too long
        long_message = "x" * 1001  # 1001 characters
        with pytest.raises(ValueError, match="Message is too long"):
            nalo_client.send_sms(phone_number="233501234567", message=long_message)

    def test_send_sms_phone_number_formatting(
        self, nalo_client, mock_requests, sms_success_response
    ):
        """Test phone number formatting for SMS."""
        mock_requests.get(
            "https://sms.nalosolutions.com/smsbackend/clientapi/Resl_Nalo/send-message",
            text="1701|233501234567|api.0039013.20250127.1753576627.8301058",
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

    def test_send_sms_unicode_message(
        self, nalo_client, mock_requests, sms_success_response
    ):
        """Test SMS with unicode characters."""
        mock_requests.get(
            "https://sms.nalosolutions.com/smsbackend/clientapi/Resl_Nalo/send-message",
            text="1701|233501234567|api.0039013.20250127.1753576627.8301058",
        )

        unicode_message = "Hello! 🇬🇭 Welcome to Ghana"

        result = nalo_client.send_sms(
            phone_number="233501234567", message=unicode_message
        )

        assert result["status"] == "success"

    def test_send_bulk_sms(self, nalo_client, mock_requests, sms_success_response):
        """Test sending bulk SMS messages."""
        mock_requests.get(
            "https://sms.nalosolutions.com/smsbackend/clientapi/Resl_Nalo/send-message",
            text="1701|233501234567|api.0039013.20250127.1753576627.8301058",
        )

        phone_numbers = ["233501234567", "233241234567", "233271234567"]
        message = "Bulk SMS test message"

        # Test sending to multiple numbers
        for phone_number in phone_numbers:
            result = nalo_client.send_sms(phone_number=phone_number, message=message)
            assert result["status"] == "success"

    def test_send_sms_with_custom_sender_id(
        self, nalo_client, mock_requests, sms_success_response
    ):
        """Test SMS with custom sender ID."""
        mock_requests.get(
            "https://sms.nalosolutions.com/smsbackend/clientapi/Resl_Nalo/send-message",
            text="1701|233501234567|api.0039013.20250127.1753576627.8301058",
        )

        result = nalo_client.send_sms(
            phone_number="233501234567",
            message="Test with custom sender",
            sender_id="CUSTOM_ID",
        )

        assert result["status"] == "success"

    @pytest.mark.api
    def test_sms_api_timeout_handling(self, nalo_client, mock_requests):
        """Test handling of SMS API timeout."""
        # Mock timeout exception
        mock_requests.get(
            "https://sms.nalosolutions.com/smsbackend/clientapi/Resl_Nalo/send-message",
            exc=requests.exceptions.Timeout,
        )

        result = nalo_client.send_sms(
            phone_number="233501234567", message="Timeout test message"
        )

        assert result["status"] == "error"
        assert "timeout" in result["message"].lower()

    @pytest.mark.api
    def test_sms_network_error_handling(self, nalo_client, mock_requests):
        """Test handling of SMS network errors."""
        # Mock network error
        mock_requests.get(
            "https://sms.nalosolutions.com/smsbackend/clientapi/Resl_Nalo/send-message",
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

    def test_sms_no_authentication_error(self, nalo_config):
        """Test SMS without authentication credentials."""
        # Remove authentication
        nalo_config["sms"]["username"] = None
        nalo_config["sms"]["password"] = None
        nalo_config["sms"]["auth_key"] = None

        client = NaloSolutions(nalo_config)

        with pytest.raises(
            ValueError, match="Authentication credentials must be provided"
        ):
            client.send_sms(phone_number="233501234567", message="Test message")
