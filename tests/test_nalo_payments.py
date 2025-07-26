"""
Tests for Nalo Solutions Payment API.
"""

import pytest
import hashlib
import requests
from unittest.mock import patch
from nunyakata.services.nalo_solutions import NaloSolutions


class TestNaloPaymentAPI:
    """Test cases for Nalo Payment API functionality."""

    def test_make_payment_success(
        self, nalo_client, mock_requests, payment_success_response
    ):
        """Test successful payment processing."""
        # Setup mock response
        mock_requests.post(
            "https://sandbox.nalosolutions.com/payment/request-payment",
            json=payment_success_response,
        )

        # Test payment
        result = nalo_client.make_payment(
            amount=10.00,
            phone_number="233501234567",
            reference="TEST_REF_001",
            description="Test payment",
            callback_url="https://example.com/callback",
        )

        # Assertions
        assert result["status"] == "success"
        assert result["transaction_id"] == "txn_12345"
        assert result["amount"] == 10.00

        # Verify request was made correctly
        assert mock_requests.called
        request = mock_requests.request_history[0]
        assert request.method == "POST"
        assert "public_key" in request.json()
        assert "secret_hash" in request.json()
        assert request.json()["amount"] == 10.00
        assert request.json()["phone_number"] == "233501234567"

    def test_make_payment_error(
        self, nalo_client, mock_requests, payment_error_response
    ):
        """Test payment processing with error."""
        # Setup mock response
        mock_requests.post(
            "https://sandbox.nalosolutions.com/payment/request-payment",
            json=payment_error_response,
            status_code=400,
        )

        # Test payment
        result = nalo_client.make_payment(
            amount=10.00, phone_number="233501234567", reference="TEST_REF_002"
        )

        # Assertions
        assert result["status"] == "error"
        assert "Insufficient funds" in result["message"]

    def test_secret_hash_generation(self, nalo_client):
        """Test that secret hash is generated correctly."""
        # Test data
        amount = 10.00
        phone_number = "233501234567"
        reference = "TEST_REF"
        private_key = "test_private_key"

        # Expected hash
        hash_string = f"{amount}{phone_number}{reference}{private_key}"
        expected_hash = hashlib.md5(hash_string.encode()).hexdigest()

        # Mock the make_payment method to access the generated hash
        with patch.object(nalo_client, "_make_request") as mock_request:
            mock_request.return_value = {"status": "success"}

            nalo_client.make_payment(
                amount=amount, phone_number=phone_number, reference=reference
            )

            # Get the request data
            call_args = mock_request.call_args
            request_data = call_args[1]["json"]

            assert request_data["secret_hash"] == expected_hash

    def test_payment_validation(self, nalo_client):
        """Test payment parameter validation."""
        # Test missing required parameters
        with pytest.raises(ValueError, match="Amount must be greater than 0"):
            nalo_client.make_payment(
                amount=None, phone_number="233501234567", reference="TEST_REF"
            )

        with pytest.raises(ValueError, match="Phone number must be provided"):
            nalo_client.make_payment(
                amount=10.00, phone_number="", reference="TEST_REF"
            )

        with pytest.raises(ValueError, match="Reference must be provided"):
            nalo_client.make_payment(
                amount=10.00, phone_number="233501234567", reference=""
            )

    def test_payment_amount_validation(self, nalo_client):
        """Test payment amount validation."""
        # Test negative amount
        with pytest.raises(ValueError, match="Amount must be greater than 0"):
            nalo_client.make_payment(
                amount=-10.00, phone_number="233501234567", reference="TEST_REF"
            )

        # Test zero amount
        with pytest.raises(ValueError, match="Amount must be greater than 0"):
            nalo_client.make_payment(
                amount=0.00, phone_number="233501234567", reference="TEST_REF"
            )

    def test_phone_number_formatting(
        self, nalo_client, mock_requests, payment_success_response
    ):
        """Test phone number formatting and validation."""
        mock_requests.post(
            "https://sandbox.nalosolutions.com/payment/request-payment",
            json=payment_success_response,
        )

        # Test various phone number formats
        test_numbers = [
            "233501234567",  # Full format
            "0501234567",  # Local format
            "+233501234567",  # International format
        ]

        for phone_number in test_numbers:
            result = nalo_client.make_payment(
                amount=10.00,
                phone_number=phone_number,
                reference=f"TEST_REF_{phone_number[-4:]}",
            )
            assert result["status"] == "success"

    def test_production_environment_url(self, nalo_config):
        """Test that production environment uses correct URL."""
        # Set production environment
        nalo_config["payment"]["environment"] = "production"
        client = NaloSolutions(nalo_config)

        with patch.object(client, "_make_request") as mock_request:
            mock_request.return_value = {"status": "success"}

            client.make_payment(
                amount=10.00, phone_number="233501234567", reference="TEST_REF"
            )

            # Verify production URL was used
            call_args = mock_request.call_args
            assert "https://api.nalosolutions.com" in call_args[0][1]

    def test_payment_with_all_optional_parameters(
        self, nalo_client, mock_requests, payment_success_response
    ):
        """Test payment with all optional parameters."""
        mock_requests.post(
            "https://sandbox.nalosolutions.com/payment/request-payment",
            json=payment_success_response,
        )

        result = nalo_client.make_payment(
            amount=50.00,
            phone_number="233501234567",
            reference="FULL_TEST_REF",
            description="Full test payment with all parameters",
            callback_url="https://example.com/payment/callback",
            metadata={"user_id": "12345", "order_id": "ORD_001"},
        )

        assert result["status"] == "success"

        # Verify all parameters were included in request
        request = mock_requests.request_history[0]
        request_data = request.json()
        assert request_data["description"] == "Full test payment with all parameters"
        assert request_data["callback_url"] == "https://example.com/payment/callback"
        assert "metadata" in request_data

    @pytest.mark.api
    def test_payment_api_timeout_handling(self, nalo_client, mock_requests):
        """Test handling of API timeout."""
        # Mock timeout exception
        mock_requests.post(
            "https://sandbox.nalosolutions.com/payment/request-payment",
            exc=requests.exceptions.Timeout,
        )

        result = nalo_client.make_payment(
            amount=10.00, phone_number="233501234567", reference="TIMEOUT_TEST"
        )

        assert result["status"] == "error"
        assert "timeout" in result["message"].lower()

    @pytest.mark.api
    def test_payment_network_error_handling(self, nalo_client, mock_requests):
        """Test handling of network errors."""
        # Mock network error
        mock_requests.post(
            "https://sandbox.nalosolutions.com/payment/request-payment",
            exc=requests.exceptions.ConnectionError,
        )

        result = nalo_client.make_payment(
            amount=10.00, phone_number="233501234567", reference="NETWORK_ERROR_TEST"
        )

        assert result["status"] == "error"
        assert (
            "network" in result["message"].lower()
            or "connection" in result["message"].lower()
        )
