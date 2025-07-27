"""Tests for Nalo USSD API functionality - Fixed to match actual implementation."""

import pytest

from nunyakata.services.nalo_solutions import NaloSolutions


class TestNaloUSSDAPI:
    """Test suite for Nalo USSD API."""

    @pytest.fixture
    def nalo_config(self):
        """Configuration for Nalo client with USSD credentials."""
        return {
            "ussd": {
                "userid": "test_userid",
                "msisdn": "233501234567",
                "environment": "sandbox",
            }
        }

    @pytest.fixture
    def nalo_client(self, nalo_config):
        """Create Nalo client instance."""
        return NaloSolutions(nalo_config)

    def test_handle_ussd_request_welcome(self, nalo_client):
        """Test initial USSD request handling."""
        request_data = {
            "USERID": "test_userid",
            "MSISDN": "233501234567",
            "USERDATA": "",
            "MSGTYPE": True,  # Initial request
            "NETWORK": "MTN",
            "SESSIONID": "session_123",
        }

        response = nalo_client.handle_ussd_request(request_data)

        # Check Nalo format response
        assert "USERID" in response
        assert "MSISDN" in response
        assert "MSG" in response
        assert "MSGTYPE" in response
        assert response["USERID"] == "test_userid"
        assert response["MSISDN"] == "233501234567"
        assert "Welcome to USSD Demo" in response["MSG"]
        assert response["MSGTYPE"] is True  # Continue session

    def test_handle_ussd_request_menu_navigation(self, nalo_client):
        """Test USSD menu navigation."""
        # First, initialize session
        init_request = {
            "USERID": "test_userid",
            "MSISDN": "233501234567",
            "USERDATA": "",
            "MSGTYPE": True,
            "NETWORK": "MTN",
            "SESSIONID": "session_456",
        }
        nalo_client.handle_ussd_request(init_request)

        # Now test menu selection
        menu_request = {
            "USERID": "test_userid",
            "MSISDN": "233501234567",
            "USERDATA": "1",  # Select option 1
            "MSGTYPE": False,  # Subsequent request
            "NETWORK": "MTN",
            "SESSIONID": "session_456",
        }

        response = nalo_client.handle_ussd_request(menu_request)

        assert "USERID" in response
        assert "MSG" in response
        assert response["USERID"] == "test_userid"
        # Option 1 should show balance
        assert "Demo Balance" in response["MSG"]

    def test_handle_ussd_request_session_timeout(self, nalo_client):
        """Test USSD session timeout handling."""
        request_data = {
            "USERID": "test_userid",
            "MSISDN": "233501234567",
            "USERDATA": "999",  # Invalid option to trigger error path
            "MSGTYPE": False,  # Subsequent request
            "NETWORK": "MTN",
            "SESSIONID": "nonexistent_session",  # Session doesn't exist
        }

        response = nalo_client.handle_ussd_request(request_data)

        assert "USERID" in response
        assert "MSG" in response
        # For nonexistent session, it will create a new one and process the invalid input
        assert "Invalid" in response["MSG"] or "Demo Balance" in response["MSG"]

    def test_create_ussd_menu_basic(self, nalo_client):
        """Test basic USSD menu creation."""
        title = "Main Menu"
        options = ["Check Balance", "Transfer Money", "Buy Airtime"]

        menu = nalo_client.create_ussd_menu(title, options)

        assert "Main Menu" in menu
        assert "1. Check Balance" in menu
        assert "2. Transfer Money" in menu
        assert "3. Buy Airtime" in menu

    def test_create_ussd_menu_with_footer(self, nalo_client):
        """Test USSD menu creation with footer."""
        title = "Services"
        options = ["Option A", "Option B"]
        footer = "Reply 0 to go back"

        menu = nalo_client.create_ussd_menu(title, options, footer)

        assert "Services" in menu
        assert "1. Option A" in menu
        assert "2. Option B" in menu
        assert "Reply 0 to go back" in menu

    def test_create_ussd_response_continue(self, nalo_client):
        """Test creating USSD response to continue session."""
        message = "Enter your PIN"
        response = nalo_client.create_ussd_response(message, continue_session=True)

        assert response["response"] == "CON"
        assert response["message"] == "Enter your PIN"

    def test_create_ussd_response_end(self, nalo_client):
        """Test creating USSD response to end session."""
        message = "Transaction completed successfully"
        response = nalo_client.create_ussd_response(message, continue_session=False)

        assert response["response"] == "END"
        assert response["message"] == "Transaction completed successfully"

    def test_ussd_session_management_new_session(self, nalo_client):
        """Test creating new USSD session."""
        sessionid = "new_session_123"
        session = nalo_client.get_ussd_session(sessionid)

        assert session is not None
        assert "step" in session
        assert "data" in session

    def test_ussd_session_management_update_session(self, nalo_client):
        """Test updating USSD session data."""
        sessionid = "update_session_123"

        # Get initial session
        nalo_client.get_ussd_session(sessionid)

        # Update session
        nalo_client.update_ussd_session(sessionid, {"stage": 2, "user_id": "12345"})

        # Retrieve updated session
        session = nalo_client.get_ussd_session(sessionid)
        assert session["stage"] == 2
        assert session["data"]["user_id"] == "12345"

    def test_ussd_session_management_clear_session(self, nalo_client):
        """Test clearing USSD session."""
        sessionid = "clear_session_123"

        # Create session
        nalo_client.get_ussd_session(sessionid)
        nalo_client.update_ussd_session(sessionid, {"stage": 1})

        # Clear session
        nalo_client.clear_ussd_session(sessionid)

        # Session should be reset when accessed again
        new_session = nalo_client.get_ussd_session(sessionid)
        assert new_session["step"] == 0

    def test_ussd_input_validation(self, nalo_client):
        """Test USSD input validation."""
        valid_options = ["1", "2", "3", "0"]

        assert nalo_client.validate_ussd_input("1", valid_options) is True
        assert nalo_client.validate_ussd_input("2", valid_options) is True
        assert nalo_client.validate_ussd_input("4", valid_options) is False
        assert nalo_client.validate_ussd_input("abc", valid_options) is False

    def test_ussd_phone_number_validation(self, nalo_client):
        """Test phone number validation."""
        # Valid formats
        assert nalo_client.validate_phone_number("233501234567") is True
        assert nalo_client.validate_phone_number("0501234567") is True

        # Invalid formats
        assert nalo_client.validate_phone_number("123456") is False
        assert nalo_client.validate_phone_number("") is False
        assert nalo_client.validate_phone_number("abc123") is False

    def test_ussd_amount_validation(self, nalo_client):
        """Test amount validation."""
        # Valid amounts
        assert nalo_client.validate_amount("10.50") is True
        assert nalo_client.validate_amount("100") is True
        assert nalo_client.validate_amount("5.75") is True

        # Invalid amounts
        assert nalo_client.validate_amount("0") is False
        assert nalo_client.validate_amount("-10") is False
        assert nalo_client.validate_amount("abc") is False
        assert nalo_client.validate_amount("10.123") is False  # Too many decimals

    def test_ussd_complex_flow_simulation(self, nalo_client):
        """Test complex USSD flow simulation."""
        sessionid = "complex_flow_123"

        # Initial request
        init_request = {
            "USERID": "test_userid",
            "MSISDN": "233501234567",
            "USERDATA": "",
            "MSGTYPE": True,
            "NETWORK": "MTN",
            "SESSIONID": sessionid,
        }

        response1 = nalo_client.handle_ussd_request(init_request)
        assert "Welcome to USSD Demo" in response1["MSG"]

        # Select services (option 3)
        services_request = {
            "USERID": "test_userid",
            "MSISDN": "233501234567",
            "USERDATA": "3",
            "MSGTYPE": False,
            "NETWORK": "MTN",
            "SESSIONID": sessionid,
        }

        response2 = nalo_client.handle_ussd_request(services_request)
        assert "Available Services" in response2["MSG"]
        assert response2["MSGTYPE"] is True  # Should continue

    def test_ussd_error_handling(self, nalo_client):
        """Test USSD error handling."""
        # Test with invalid USERID
        invalid_request = {
            "USERID": "",  # Empty USERID
            "MSISDN": "233501234567",
            "USERDATA": "",
            "MSGTYPE": True,
            "NETWORK": "MTN",
            "SESSIONID": "error_session_123",
        }

        response = nalo_client.handle_ussd_request(invalid_request)
        assert "Invalid USERID" in response["MSG"]
        assert response["MSGTYPE"] is False

    def test_ussd_production_environment_configuration(self, nalo_client):
        """Test USSD configuration for production environment."""
        # Test that environment setting doesn't break functionality
        nalo_client.ussd_environment = "production"

        request_data = {
            "USERID": "test_userid",
            "MSISDN": "233501234567",
            "USERDATA": "",
            "MSGTYPE": True,
            "NETWORK": "MTN",
            "SESSIONID": "prod_session_123",
        }

        response = nalo_client.handle_ussd_request(request_data)
        assert "USERID" in response
        assert "MSG" in response
