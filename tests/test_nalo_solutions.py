"""
Tests for Nalo Solutions client.
"""

import pytest
from unittest.mock import Mock, patch
from nunyakata.services.nalo_solutions import NaloSolutionsClient


class TestNaloSolutionsClient:
    """Test cases for NaloSolutionsClient."""

    def test_init_with_api_key(self):
        """Test client initialization with API key."""
        client = NaloSolutionsClient(api_key="test_key")
        assert client.api_key == "test_key"
        assert "Authorization" in client.session.headers

    def test_init_without_api_key(self):
        """Test client initialization without API key."""
        client = NaloSolutionsClient()
        assert client.api_key is None
        assert "Authorization" not in client.session.headers

    @patch("requests.Session.get")
    def test_get_service_status(self, mock_get):
        """Test getting service status."""
        # Mock the response
        mock_response = Mock()
        mock_response.json.return_value = {"status": "active"}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        client = NaloSolutionsClient()
        result = client.get_service_status()

        assert result == {"status": "active"}
        mock_get.assert_called_once()

    @patch("requests.Session.post")
    def test_send_sms(self, mock_post):
        """Test sending SMS."""
        # Mock the response
        mock_response = Mock()
        mock_response.json.return_value = {"message_id": "123", "status": "sent"}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        client = NaloSolutionsClient(api_key="test_key")
        result = client.send_sms("233123456789", "Test message")

        assert result == {"message_id": "123", "status": "sent"}
        mock_post.assert_called_once()
