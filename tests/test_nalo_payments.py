"""Tests for Nalo Payment API functionality - Fixed to match actual implementation."""

import pytest
import requests

from nunyakata.services.nalo_solutions import NaloSolutions


class TestNaloPaymentAPI:
    """Test suite for Nalo Payment API."""

    @pytest.fixture
    def nalo_config(self):
        """Configuration for Nalo client with payment credentials."""
        return {
            "payment": {
                "merchant_id": "test_merchant_123",
                "username": "test_user",
                "password": "test_password",
                "environment": "production",
            }
        }

    @pytest.fixture
    def nalo_client(self, nalo_config):
        """Create Nalo client instance."""
        return NaloSolutions(nalo_config)

    @pytest.fixture
    def payment_success_response(self):
        """Mock successful payment response."""
        return {
            "status": "success",
            "message": "Payment successful",
            "order_id": "ORDER123",
            "amount": 10.0,
        }

    @pytest.fixture
    def payment_error_response(self):
        """Mock payment error response."""
        return {
            "status": "error",
            "message": "Insufficient funds",
            "code": "INSUFFICIENT_FUNDS",
        }

    def test_make_payment_success(
        self, nalo_client, mock_requests, payment_success_response
    ):
        """Test successful payment processing."""
        # Setup mock response
        mock_requests.post(
            "https://api.nalosolutions.com/payplus/api",
            json=payment_success_response,
        )

        # Test payment
        result = nalo_client.make_payment(
            amount=10.00,
            customer_number="233501234567",
            customer_name="Test Customer",
            item_desc="Test payment",
            order_id="TEST_ORDER_001",
            payby="MTN",
            callback_url="https://example.com/callback",
        )

        # Assertions
        assert result["status"] == "success"
        assert result["order_id"] == "ORDER123"
        assert result["amount"] == 10.0

    def test_make_payment_error(
        self, nalo_client, mock_requests, payment_error_response
    ):
        """Test payment processing with error."""
        # Setup mock response
        mock_requests.post(
            "https://api.nalosolutions.com/payplus/api",
            json=payment_error_response,
            status_code=400,
        )

        # Test payment
        result = nalo_client.make_payment(
            amount=10.00,
            customer_number="233501234567",
            customer_name="Test Customer",
            item_desc="Test payment",
            order_id="TEST_ORDER_002",
            payby="MTN",
            callback_url="https://example.com/callback",
        )

        # Assertions
        assert result["status"] == "error"
        assert "Insufficient funds" in result["message"]

    def test_payment_validation(self, nalo_client):
        """Test payment parameter validation."""
        # Test missing required parameters
        with pytest.raises(ValueError, match="Amount must be greater than 0"):
            nalo_client.make_payment(
                amount=None,
                customer_number="233501234567",
                customer_name="Test Customer",
                item_desc="Test payment",
                order_id="TEST_ORDER",
                payby="MTN",
                callback_url="https://example.com/callback",
            )

    def test_payment_amount_validation(self, nalo_client):
        """Test payment amount validation."""
        # Test negative amount
        with pytest.raises(ValueError, match="Amount must be greater than 0"):
            nalo_client.make_payment(
                amount=-10.00,
                customer_number="233501234567",
                customer_name="Test Customer",
                item_desc="Test payment",
                order_id="TEST_ORDER",
                payby="MTN",
                callback_url="https://example.com/callback",
            )

    def test_payby_validation(self, nalo_client):
        """Test payby parameter validation."""
        # Test invalid payby
        with pytest.raises(
            ValueError, match="payby must be one of: MTN, AIRTELTIGO, VODAFONE"
        ):
            nalo_client.make_payment(
                amount=10.00,
                customer_number="233501234567",
                customer_name="Test Customer",
                item_desc="Test payment",
                order_id="TEST_ORDER",
                payby="INVALID_NETWORK",
                callback_url="https://example.com/callback",
            )

    def test_make_simple_payment_success(
        self, nalo_client, mock_requests, payment_success_response
    ):
        """Test simplified payment method."""
        mock_requests.post(
            "https://api.nalosolutions.com/payplus/api",
            json=payment_success_response,
        )

        result = nalo_client.make_simple_payment(
            amount=10.00,
            phone_number="233501234567",
            customer_name="Test Customer",
            description="Test simple payment",
            callback_url="https://example.com/callback",
        )

        assert result["status"] == "success"

    def test_network_detection(
        self, nalo_client, mock_requests, payment_success_response
    ):
        """Test automatic network detection."""
        mock_requests.post(
            "https://api.nalosolutions.com/payplus/api",
            json=payment_success_response,
        )

        # Test MTN number
        result = nalo_client.make_simple_payment(
            amount=10.00,
            phone_number="233544123456",  # MTN
            customer_name="Test Customer",
            description="Test MTN payment",
            callback_url="https://example.com/callback",
        )
        assert result["status"] == "success"

        # Test Vodafone number
        result = nalo_client.make_simple_payment(
            amount=10.00,
            phone_number="233201234567",  # Vodafone
            customer_name="Test Customer",
            description="Test Vodafone payment",
            callback_url="https://example.com/callback",
        )
        assert result["status"] == "success"

    def test_payment_callback_handling(self, nalo_client):
        """Test payment callback handling."""
        callback_data = {
            "Timestamp": "2024-01-01T10:00:00Z",
            "Status": "PAID",
            "InvoiceNo": "INV123",
            "Order_id": "ORDER123",
        }

        result = nalo_client.handle_payment_callback(callback_data)
        assert result["Response"] == "OK"

    def test_payment_callback_error(self, nalo_client):
        """Test payment callback with missing data."""
        callback_data = {
            "Status": "PAID",
            # Missing required fields
        }

        result = nalo_client.handle_payment_callback(callback_data)
        assert result["Response"] == "ERROR"
        assert "Invalid callback data" in result["message"]

    @pytest.mark.api
    def test_payment_api_timeout_handling(self, nalo_client, mock_requests):
        """Test handling of API timeout."""
        # Mock timeout exception
        mock_requests.post(
            "https://api.nalosolutions.com/payplus/api",
            exc=requests.exceptions.Timeout,
        )

        result = nalo_client.make_payment(
            amount=10.00,
            customer_number="233501234567",
            customer_name="Test Customer",
            item_desc="Timeout test",
            order_id="TIMEOUT_TEST",
            payby="MTN",
            callback_url="https://example.com/callback",
        )

        assert result["status"] == "error"
        assert "timeout" in result["message"].lower()

    @pytest.mark.api
    def test_payment_network_error_handling(self, nalo_client, mock_requests):
        """Test handling of network errors."""
        # Mock network error
        mock_requests.post(
            "https://api.nalosolutions.com/payplus/api",
            exc=requests.exceptions.ConnectionError,
        )

        result = nalo_client.make_payment(
            amount=10.00,
            customer_number="233501234567",
            customer_name="Test Customer",
            item_desc="Network error test",
            order_id="NETWORK_ERROR_TEST",
            payby="MTN",
            callback_url="https://example.com/callback",
        )

        assert result["status"] == "error"
        assert (
            "network" in result["message"].lower()
            or "connection" in result["message"].lower()
        )
