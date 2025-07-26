"""
Tests for Nalo Solutions USSD API.
"""

import pytest
from nunyakata.services.nalo_solutions import NaloSolutions


class TestNaloUSSDAPI:
    """Test cases for Nalo USSD API functionality."""

    def test_handle_ussd_request_welcome(self, nalo_client, ussd_session_data):
        """Test handling initial USSD request (welcome message)."""
        # Simulate initial USSD request
        session_data = ussd_session_data.copy()
        session_data["msg"] = ""  # Empty message for initial request

        response = nalo_client.handle_ussd_request(session_data)

        assert response["response"] == "CON"
        assert "Welcome" in response["message"]
        assert response["sessionid"] == "sess_12345"

    def test_handle_ussd_request_menu_navigation(self, nalo_client, ussd_session_data):
        """Test USSD menu navigation."""
        # Test menu option selection
        session_data = ussd_session_data.copy()
        session_data["msg"] = "1"  # Select option 1

        response = nalo_client.handle_ussd_request(session_data)

        assert response["response"] in ["CON", "END"]
        assert response["sessionid"] == "sess_12345"
        assert "message" in response

    def test_handle_ussd_request_session_timeout(self, nalo_client, ussd_session_data):
        """Test USSD session timeout handling."""
        # Simulate expired session
        session_data = ussd_session_data.copy()
        session_data["msgtype"] = False  # Session ended

        response = nalo_client.handle_ussd_request(session_data)

        assert response["response"] == "END"
        assert (
            "session" in response["message"].lower()
            or "timeout" in response["message"].lower()
        )

    def test_create_ussd_menu_basic(self, nalo_client):
        """Test creating basic USSD menu."""
        title = "Main Menu"
        options = ["Check Balance", "Send Money", "Buy Airtime", "Exit"]

        menu = nalo_client.create_ussd_menu(title, options)

        assert title in menu
        assert "1. Check Balance" in menu
        assert "2. Send Money" in menu
        assert "3. Buy Airtime" in menu
        assert "4. Exit" in menu

    def test_create_ussd_menu_with_footer(self, nalo_client):
        """Test creating USSD menu with footer."""
        title = "Services"
        options = ["Option 1", "Option 2"]
        footer = "Reply with option number"

        menu = nalo_client.create_ussd_menu(title, options, footer)

        assert title in menu
        assert "1. Option 1" in menu
        assert "2. Option 2" in menu
        assert footer in menu

    def test_create_ussd_response_continue(self, nalo_client):
        """Test creating USSD continue response."""
        message = "Enter your PIN:"

        response = nalo_client.create_ussd_response(message, continue_session=True)

        assert response["response"] == "CON"
        assert response["message"] == message

    def test_create_ussd_response_end(self, nalo_client):
        """Test creating USSD end response."""
        message = "Thank you for using our service!"

        response = nalo_client.create_ussd_response(message, continue_session=False)

        assert response["response"] == "END"
        assert response["message"] == message

    def test_ussd_session_management_new_session(self, nalo_client):
        """Test USSD session management for new sessions."""
        sessionid = "new_session_123"

        # Check that new session is properly initialized
        session_data = nalo_client.get_ussd_session(sessionid)

        assert session_data is not None
        assert session_data.get("step", 0) == 0
        assert session_data.get("data", {}) == {}

    def test_ussd_session_management_update_session(self, nalo_client):
        """Test updating USSD session data."""
        sessionid = "update_session_123"

        # Initialize session
        nalo_client.get_ussd_session(sessionid)

        # Update session with new data
        update_data = {
            "step": 2,
            "selected_service": "balance_inquiry",
            "phone_number": "233501234567",
        }
        nalo_client.update_ussd_session(sessionid, update_data)

        # Verify update
        session_data = nalo_client.get_ussd_session(sessionid)
        assert session_data["step"] == 2
        assert session_data["data"]["selected_service"] == "balance_inquiry"
        assert session_data["data"]["phone_number"] == "233501234567"

    def test_ussd_session_management_clear_session(self, nalo_client):
        """Test clearing USSD session."""
        sessionid = "clear_session_123"

        # Initialize and update session
        nalo_client.get_ussd_session(sessionid)
        nalo_client.update_ussd_session(
            sessionid, {"step": 5, "data": {"test": "value"}}
        )

        # Clear session
        nalo_client.clear_ussd_session(sessionid)

        # Verify session is cleared (new session should be created)
        session_data = nalo_client.get_ussd_session(sessionid)
        assert session_data["step"] == 0
        assert session_data["data"] == {}

    def test_ussd_input_validation(self, nalo_client):
        """Test USSD input validation."""
        # Test valid numeric input
        assert nalo_client.validate_ussd_input("1", ["1", "2", "3"]) == True
        assert nalo_client.validate_ussd_input("2", ["1", "2", "3"]) == True

        # Test invalid input
        assert nalo_client.validate_ussd_input("4", ["1", "2", "3"]) == False
        assert nalo_client.validate_ussd_input("abc", ["1", "2", "3"]) == False
        assert nalo_client.validate_ussd_input("", ["1", "2", "3"]) == False

    def test_ussd_phone_number_validation(self, nalo_client):
        """Test USSD phone number validation."""
        # Valid phone numbers
        valid_numbers = ["233501234567", "0501234567", "+233501234567"]

        for number in valid_numbers:
            assert nalo_client.validate_phone_number(number) == True

        # Invalid phone numbers
        invalid_numbers = [
            "123",
            "abcd1234567",
            "233501234",  # Too short
            "2335012345678901",  # Too long
            "",
        ]

        for number in invalid_numbers:
            assert nalo_client.validate_phone_number(number) == False

    def test_ussd_amount_validation(self, nalo_client):
        """Test USSD amount validation."""
        # Valid amounts
        valid_amounts = ["10.00", "100", "0.50", "1000.99"]

        for amount in valid_amounts:
            assert nalo_client.validate_amount(amount) == True

        # Invalid amounts
        invalid_amounts = [
            "abc",
            "-10",
            "0",
            "",
            "10.001",
        ]  # More than 2 decimal places

        for amount in invalid_amounts:
            assert nalo_client.validate_amount(amount) == False

    def test_ussd_complex_flow_simulation(self, nalo_client):
        """Test complex USSD flow simulation."""
        sessionid = "complex_flow_123"
        msisdn = "233501234567"
        userid = "test_userid"

        # Step 1: Initial request
        session_data = {
            "sessionid": sessionid,
            "msisdn": msisdn,
            "userid": userid,
            "msg": "",
            "msgtype": True,
        }

        response1 = nalo_client.handle_ussd_request(session_data)
        assert response1["response"] == "CON"
        assert "Welcome" in response1["message"]

        # Step 2: Select service
        session_data["msg"] = "1"  # Select balance inquiry
        response2 = nalo_client.handle_ussd_request(session_data)
        assert response2["response"] in ["CON", "END"]

        # Step 3: Continue flow based on response
        if response2["response"] == "CON":
            session_data["msg"] = "1234"  # Enter PIN
            response3 = nalo_client.handle_ussd_request(session_data)
            assert "response" in response3

    def test_ussd_error_handling(self, nalo_client):
        """Test USSD error handling."""
        # Test with invalid session data
        invalid_session_data = {
            "sessionid": "",  # Empty session ID
            "msisdn": "invalid_number",
            "userid": "",
            "msg": "test",
            "msgtype": True,
        }

        response = nalo_client.handle_ussd_request(invalid_session_data)
        assert response["response"] == "END"
        assert "error" in response["message"].lower()

    def test_ussd_sandbox_environment_handling(self, nalo_config):
        """Test USSD sandbox environment configuration."""
        # Verify sandbox configuration
        assert nalo_config["ussd"]["environment"] == "sandbox"

        client = NaloSolutions(nalo_config)

        # Test that sandbox mode doesn't affect basic functionality
        session_data = {
            "sessionid": "sandbox_test",
            "msisdn": "233501234567",
            "userid": "test_userid",
            "msg": "",
            "msgtype": True,
        }

        response = client.handle_ussd_request(session_data)
        assert "response" in response
        assert "message" in response

    def test_ussd_production_environment_configuration(self, nalo_config):
        """Test USSD production environment configuration."""
        # Set production environment
        nalo_config["ussd"]["environment"] = "production"
        client = NaloSolutions(nalo_config)

        # Verify production configuration is properly set
        assert client.config["ussd"]["environment"] == "production"

    @pytest.mark.integration
    def test_ussd_webhook_integration(self, nalo_client):
        """Test USSD webhook integration simulation."""
        # Simulate webhook data
        webhook_data = {
            "sessionid": "webhook_test_123",
            "msisdn": "233501234567",
            "userid": "test_userid",
            "msg": "1",
            "msgtype": True,
        }

        # Process webhook request
        response = nalo_client.handle_ussd_request(webhook_data)

        # Verify response format for webhook
        assert isinstance(response, dict)
        assert "response" in response
        assert "message" in response
        assert response["response"] in ["CON", "END"]

    @pytest.mark.slow
    def test_ussd_session_persistence(self, nalo_client):
        """Test USSD session persistence across multiple requests."""
        sessionid = "persistence_test_123"

        # Multiple requests with same session
        for step in range(5):
            session_data = {
                "sessionid": sessionid,
                "msisdn": "233501234567",
                "userid": "test_userid",
                "msg": str(step),
                "msgtype": True,
            }

            response = nalo_client.handle_ussd_request(session_data)

            # Verify session is maintained
            current_session = nalo_client.get_ussd_session(sessionid)
            assert current_session is not None

            if response["response"] == "END":
                break
