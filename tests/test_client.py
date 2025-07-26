"""
Tests for the NunyakataClient class.
"""

import pytest
from unittest.mock import Mock, patch
from nunyakata import NunyakataClient


class TestNunyakataClient:
    """Test cases for NunyakataClient."""

    def test_client_initialization(self):
        """Test client can be initialized with default parameters."""
        client = NunyakataClient()
        assert client.base_url == "https://api.example.com"
        assert client.api_key is None

    def test_client_initialization_with_api_key(self):
        """Test client can be initialized with API key."""
        api_key = "test-api-key"
        client = NunyakataClient(api_key=api_key)
        assert client.api_key == api_key
        assert "Authorization" in client.session.headers

    def test_client_initialization_with_base_url(self):
        """Test client can be initialized with custom base URL."""
        base_url = "https://custom-api.example.com"
        client = NunyakataClient(base_url=base_url)
        assert client.base_url == base_url

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
