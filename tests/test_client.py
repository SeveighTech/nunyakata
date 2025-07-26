"""
Tests for NunyakataClient main client.
"""

import pytest
from nunyakata.client import NunyakataClient
from nunyakata.services.nalo_solutions import NaloSolutions


class TestNunyakataClient:
    """Test cases for the main NunyakataClient class."""

    def test_client_initialization(self, nunyakata_client):
        """Test that client initializes correctly."""
        assert isinstance(nunyakata_client, NunyakataClient)
        assert hasattr(nunyakata_client, "services")
        assert nunyakata_client.services == {}

    def test_add_service(self, nunyakata_client, nalo_config):
        """Test adding a service to the client."""
        nalo_service = NaloSolutions(nalo_config)

        nunyakata_client.add_service("nalo", nalo_service)

        assert "nalo" in nunyakata_client.services
        assert isinstance(nunyakata_client.services["nalo"], NaloSolutions)

    def test_get_service(self, nunyakata_client, nalo_config):
        """Test getting a service from the client."""
        nalo_service = NaloSolutions(nalo_config)
        nunyakata_client.add_service("nalo", nalo_service)

        retrieved_service = nunyakata_client.get_service("nalo")

        assert retrieved_service is nalo_service
        assert isinstance(retrieved_service, NaloSolutions)

    def test_get_nonexistent_service(self, nunyakata_client):
        """Test getting a service that doesn't exist."""
        with pytest.raises(KeyError, match="Service 'nonexistent' not found"):
            nunyakata_client.get_service("nonexistent")

    def test_list_services(self, nunyakata_client, nalo_config):
        """Test listing all services."""
        # Initially empty
        assert nunyakata_client.list_services() == []

        # Add a service
        nalo_service = NaloSolutions(nalo_config)
        nunyakata_client.add_service("nalo", nalo_service)

        services = nunyakata_client.list_services()
        assert "nalo" in services
        assert len(services) == 1

    def test_remove_service(self, nunyakata_client, nalo_config):
        """Test removing a service from the client."""
        nalo_service = NaloSolutions(nalo_config)
        nunyakata_client.add_service("nalo", nalo_service)

        # Verify service exists
        assert "nalo" in nunyakata_client.services

        # Remove service
        nunyakata_client.remove_service("nalo")

        # Verify service is removed
        assert "nalo" not in nunyakata_client.services

    def test_remove_nonexistent_service(self, nunyakata_client):
        """Test removing a service that doesn't exist."""
        with pytest.raises(KeyError, match="Service 'nonexistent' not found"):
            nunyakata_client.remove_service("nonexistent")

    def test_client_with_multiple_services(self, nunyakata_client, nalo_config):
        """Test client with multiple services."""
        # Add multiple instances with different configs
        nalo_service1 = NaloSolutions(nalo_config)
        nalo_service2 = NaloSolutions(nalo_config)

        nunyakata_client.add_service("nalo_primary", nalo_service1)
        nunyakata_client.add_service("nalo_secondary", nalo_service2)

        services = nunyakata_client.list_services()
        assert len(services) == 2
        assert "nalo_primary" in services
        assert "nalo_secondary" in services

    def test_service_replacement(self, nunyakata_client, nalo_config):
        """Test replacing an existing service."""
        nalo_service1 = NaloSolutions(nalo_config)
        nalo_service2 = NaloSolutions(nalo_config)

        # Add first service
        nunyakata_client.add_service("nalo", nalo_service1)
        assert nunyakata_client.get_service("nalo") is nalo_service1

        # Replace with second service
        nunyakata_client.add_service("nalo", nalo_service2)
        assert nunyakata_client.get_service("nalo") is nalo_service2
        assert nunyakata_client.get_service("nalo") is not nalo_service1

    def test_client_service_validation(self, nunyakata_client):
        """Test that client validates service types."""
        # Try to add an invalid service
        with pytest.raises(
            TypeError, match="Service must be an instance of a valid service class"
        ):
            nunyakata_client.add_service("invalid", "not_a_service")

    def test_client_context_manager(self, nalo_config):
        """Test using client as context manager."""
        with NunyakataClient() as client:
            nalo_service = NaloSolutions(nalo_config)
            client.add_service("nalo", nalo_service)

            assert "nalo" in client.services
            assert isinstance(client.get_service("nalo"), NaloSolutions)

    def test_client_string_representation(self, nunyakata_client, nalo_config):
        """Test string representation of client."""
        # Empty client
        assert "NunyakataClient(services=0)" in str(nunyakata_client)

        # With services
        nalo_service = NaloSolutions(nalo_config)
        nunyakata_client.add_service("nalo", nalo_service)

        assert "NunyakataClient(services=1)" in str(nunyakata_client)

    def test_client_service_method_delegation(
        self, nunyakata_client, nalo_config, mock_requests, payment_success_response
    ):
        """Test that client can delegate method calls to services."""
        # Add Nalo service
        nalo_service = NaloSolutions(nalo_config)
        nunyakata_client.add_service("nalo", nalo_service)

        # Mock payment response
        mock_requests.post(
            "https://sandbox.nalosolutions.com/payment/request-payment",
            json=payment_success_response,
        )

        # Access service through client and make payment
        nalo = nunyakata_client.get_service("nalo")
        result = nalo.make_payment(
            amount=10.00, phone_number="233501234567", reference="CLIENT_TEST_001"
        )

        assert result["status"] == "success"
        assert result["transaction_id"] == "txn_12345"

    @pytest.mark.unit
    def test_client_configuration_management(self, nunyakata_client):
        """Test client configuration management."""
        # Test setting global configuration
        config = {"timeout": 30, "retry_attempts": 3, "debug": True}

        nunyakata_client.set_global_config(config)

        assert nunyakata_client.global_config["timeout"] == 30
        assert nunyakata_client.global_config["retry_attempts"] == 3
        assert nunyakata_client.global_config["debug"] is True

    @pytest.mark.unit
    def test_client_error_handling(self, nunyakata_client):
        """Test client error handling."""
        # Test with invalid service name
        with pytest.raises(ValueError, match="Service name must be a non-empty string"):
            nunyakata_client.add_service("", None)

        with pytest.raises(ValueError, match="Service name must be a non-empty string"):
            nunyakata_client.add_service(None, None)

    def test_get_service_status(self):
        """Test get_service_status returns expected structure."""
        client = NunyakataClient()
        status = client.get_service_status()
        assert isinstance(status, dict)
        assert "status" in status
        assert "services" in status

    def test_context_manager(self):
        """Test client can be used as context manager."""
        with NunyakataClient() as client:
            assert client is not None
            status = client.get_service_status()
            assert isinstance(status, dict)
