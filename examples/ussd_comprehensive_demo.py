"""
Comprehensive USSD Example for Nalo Solutions

This example demonstrates how to build a complete USSD application using the
Nalo Solutions USSD API. It includes session management, menu navigation,
and proper response formatting according to the official documentation.

Based on Nalo Solutions USSD API Documentation.
"""

from typing import Dict, Any, Optional
from nunyakata import NaloSolutionsClient


class MyUSSDApplication:
    """
    Example USSD application with session management.

    This demonstrates how to build a complete USSD service using
    Nalo Solutions USSD API with proper session handling.
    """

    def __init__(self):
        """Initialize the USSD application."""
        self.sessions = {}  # In production, use Redis or database for session storage

    def handle_ussd_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle incoming USSD request with session management.

        Args:
            request_data: USSD request from Nalo Solutions

        Returns:
            USSD response formatted for Nalo Solutions
        """
        # Extract request parameters according to Nalo documentation
        userid = request_data.get("USERID")
        msisdn = request_data.get("MSISDN")
        user_data = request_data.get("USERDATA", "")
        msgtype = request_data.get("MSGTYPE")
        sessionid = request_data.get("SESSIONID")
        network = request_data.get("NETWORK")

        # Validate required parameters
        if not userid:
            return self._create_error_response("Invalid request: USERID required")

        # Use MSISDN as session key (as recommended in Nalo docs)
        session_key = msisdn or sessionid

        if msgtype is True:  # Initial dial
            # Clear any existing session and start fresh
            if session_key in self.sessions:
                del self.sessions[session_key]

            return self._handle_initial_request(userid, msisdn, user_data)

        else:  # Continuing session
            return self._handle_continuing_session(
                userid, msisdn, user_data, session_key or "default", network
            )

    def _handle_initial_request(
        self, userid: str, msisdn: Optional[str], user_data: str
    ) -> Dict[str, Any]:
        """Handle initial USSD dial."""
        # Initialize session
        session_key = msisdn
        self.sessions[session_key] = {
            "screen": "main_menu",
            "history": [user_data],
            "user_data": {},
        }

        # Main menu
        menu_text = (
            "Welcome to MyBank USSD\\n"
            "Select an option:\\n"
            "1. Check Balance\\n"
            "2. Transfer Money\\n"
            "3. Buy Airtime\\n"
            "4. Account Info\\n"
            "0. Exit"
        )

        return {
            "USERID": userid,
            "MSISDN": msisdn,
            "MSG": menu_text,
            "MSGTYPE": True,  # Continue session
        }

    def _handle_continuing_session(
        self,
        userid: str,
        msisdn: Optional[str],
        user_data: str,
        session_key: str,
        network: Optional[str],
    ) -> Dict[str, Any]:
        """Handle continuing USSD session."""
        # Get session data
        session = self.sessions.get(session_key, {})
        if not session:
            # Session expired or not found, restart
            return self._handle_initial_request(userid, msisdn, "")

        # Update session history
        session["history"].append(user_data)
        current_screen = session.get("screen", "main_menu")

        # Route to appropriate handler based on current screen
        if current_screen == "main_menu":
            return self._handle_main_menu(
                userid, msisdn, user_data, session_key, network
            )
        elif current_screen == "balance":
            return self._handle_balance_screen(userid, msisdn, user_data, session_key)
        elif current_screen == "transfer":
            return self._handle_transfer_screen(userid, msisdn, user_data, session_key)
        elif current_screen == "airtime":
            return self._handle_airtime_screen(userid, msisdn, user_data, session_key)
        elif current_screen == "account_info":
            return self._handle_account_info(
                userid, msisdn, user_data, session_key, network
            )
        else:
            return self._create_error_response("Session error occurred")

    def _handle_main_menu(
        self,
        userid: str,
        msisdn: Optional[str],
        user_data: str,
        session_key: str,
        network: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Handle main menu selection."""
        if user_data == "1":
            # Check Balance
            self.sessions[session_key]["screen"] = "balance"
            return {
                "USERID": userid,
                "MSISDN": msisdn,
                "MSG": "Checking your balance...\\nYour current balance is GHS 150.50\\n\\nPress any key to return to main menu",
                "MSGTYPE": True,
            }
        elif user_data == "2":
            # Transfer Money
            self.sessions[session_key]["screen"] = "transfer"
            return {
                "USERID": userid,
                "MSISDN": msisdn,
                "MSG": "Money Transfer\\nEnter recipient's phone number\\n(format: 233XXXXXXXXX):",
                "MSGTYPE": True,
            }
        elif user_data == "3":
            # Buy Airtime
            self.sessions[session_key]["screen"] = "airtime"
            return {
                "USERID": userid,
                "MSISDN": msisdn,
                "MSG": f"Buy Airtime for {network or 'your network'}\\nEnter amount (GHS):",
                "MSGTYPE": True,
            }
        elif user_data == "4":
            # Account Info
            self.sessions[session_key]["screen"] = "account_info"
            return {
                "USERID": userid,
                "MSISDN": msisdn,
                "MSG": f"Account Information\\nPhone: {msisdn}\\nNetwork: {network or 'Unknown'}\\nAccount Type: Savings\\n\\nPress any key to continue",
                "MSGTYPE": True,
            }
        elif user_data == "0":
            # Exit
            if session_key in self.sessions:
                del self.sessions[session_key]
            return {
                "USERID": userid,
                "MSISDN": msisdn,
                "MSG": "Thank you for using MyBank USSD service!\\nHave a great day!",
                "MSGTYPE": False,  # Terminate session
            }
        else:
            return {
                "USERID": userid,
                "MSISDN": msisdn,
                "MSG": "Invalid option. Please try again.\\nSelect: 1, 2, 3, 4, or 0",
                "MSGTYPE": True,
            }

    def _handle_balance_screen(
        self, userid: str, msisdn: Optional[str], user_data: str, session_key: str
    ) -> Dict[str, Any]:
        """Handle balance inquiry screen."""
        # Return to main menu
        self.sessions[session_key]["screen"] = "main_menu"
        return self._handle_initial_request(userid, msisdn, "")

    def _handle_transfer_screen(
        self, userid: str, msisdn: Optional[str], user_data: str, session_key: str
    ) -> Dict[str, Any]:
        """Handle money transfer flow."""
        session = self.sessions[session_key]

        if "recipient" not in session["user_data"]:
            # Validate phone number
            if len(user_data) == 12 and user_data.startswith("233"):
                session["user_data"]["recipient"] = user_data
                return {
                    "USERID": userid,
                    "MSISDN": msisdn,
                    "MSG": f"Transfer to {user_data}\\nEnter amount (GHS):",
                    "MSGTYPE": True,
                }
            else:
                return {
                    "USERID": userid,
                    "MSISDN": msisdn,
                    "MSG": "Invalid phone number format.\\nPlease enter 233XXXXXXXXX:",
                    "MSGTYPE": True,
                }
        elif "amount" not in session["user_data"]:
            # Validate amount
            try:
                amount = float(user_data)
                if amount > 0 and amount <= 1000:  # Max transfer limit
                    session["user_data"]["amount"] = amount
                    recipient = session["user_data"]["recipient"]
                    return {
                        "USERID": userid,
                        "MSISDN": msisdn,
                        "MSG": f"Confirm Transfer\\nTo: {recipient}\\nAmount: GHS {amount:.2f}\\n\\n1. Confirm\\n2. Cancel",
                        "MSGTYPE": True,
                    }
                else:
                    return {
                        "USERID": userid,
                        "MSISDN": msisdn,
                        "MSG": "Invalid amount. Enter amount between GHS 1-1000:",
                        "MSGTYPE": True,
                    }
            except ValueError:
                return {
                    "USERID": userid,
                    "MSISDN": msisdn,
                    "MSG": "Invalid amount format. Enter numeric value:",
                    "MSGTYPE": True,
                }
        else:
            # Confirmation
            if user_data == "1":
                recipient = session["user_data"]["recipient"]
                amount = session["user_data"]["amount"]
                # In real implementation, process the transfer here
                self.sessions[session_key]["screen"] = "main_menu"
                return {
                    "USERID": userid,
                    "MSISDN": msisdn,
                    "MSG": f"Transfer Successful!\\nGHS {amount:.2f} sent to {recipient}\\nTransaction ID: TXN123456\\n\\nPress any key to continue",
                    "MSGTYPE": True,
                }
            else:
                # Cancel transfer, return to main menu
                self.sessions[session_key]["screen"] = "main_menu"
                return {
                    "USERID": userid,
                    "MSISDN": msisdn,
                    "MSG": "Transfer cancelled.\\nReturning to main menu...",
                    "MSGTYPE": True,
                }

    def _handle_airtime_screen(
        self, userid: str, msisdn: Optional[str], user_data: str, session_key: str
    ) -> Dict[str, Any]:
        """Handle airtime purchase."""
        try:
            amount = float(user_data)
            if amount >= 1 and amount <= 100:
                # Process airtime purchase
                self.sessions[session_key]["screen"] = "main_menu"
                return {
                    "USERID": userid,
                    "MSISDN": msisdn,
                    "MSG": f"Airtime Purchase Successful!\\nGHS {amount:.2f} airtime added to {msisdn}\\n\\nPress any key to continue",
                    "MSGTYPE": True,
                }
            else:
                return {
                    "USERID": userid,
                    "MSISDN": msisdn,
                    "MSG": "Invalid amount. Enter amount between GHS 1-100:",
                    "MSGTYPE": True,
                }
        except ValueError:
            return {
                "USERID": userid,
                "MSISDN": msisdn,
                "MSG": "Invalid amount format. Enter numeric value:",
                "MSGTYPE": True,
            }

    def _handle_account_info(
        self,
        userid: str,
        msisdn: Optional[str],
        user_data: str,
        session_key: str,
        network: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Handle account information screen."""
        # Return to main menu
        self.sessions[session_key]["screen"] = "main_menu"
        return self._handle_initial_request(userid, msisdn, "")

    def _create_error_response(self, message: str) -> Dict[str, Any]:
        """Create error response."""
        return {"USERID": "ERROR", "MSG": f"Error: {message}", "MSGTYPE": False}


# === FLASK WEBHOOK EXAMPLE ===


def create_ussd_webhook_app():
    """
    Create a Flask app to handle USSD webhooks from Nalo Solutions.

    This demonstrates how to integrate the USSD handler with a web framework.
    """
    try:
        from flask import Flask, request, jsonify
    except ImportError:
        print("Flask not installed. Install with: pip install flask")
        return None

    app = Flask(__name__)
    ussd_app = MyUSSDApplication()

    @app.route("/ussd-webhook", methods=["POST"])
    def handle_ussd_webhook():
        """Handle incoming USSD webhook from Nalo Solutions."""
        try:
            # Get JSON data from request
            ussd_data = request.get_json()

            if not ussd_data:
                return jsonify({"error": "No JSON data received"}), 400

            # Process USSD request
            response = ussd_app.handle_ussd_request(ussd_data)

            # Return JSON response
            return jsonify(response)

        except Exception:
            # Log error in production
            error_response = {
                "USERID": ussd_data.get("USERID", "ERROR") if ussd_data else "ERROR",
                "MSG": "Service temporarily unavailable. Please try again later.",
                "MSGTYPE": False,
            }
            return jsonify(error_response), 500

    @app.route("/health", methods=["GET"])
    def health_check():
        """Health check endpoint."""
        return jsonify({"status": "healthy", "service": "USSD Webhook"})

    return app


# === USAGE EXAMPLES ===


def main():
    """Demonstrate USSD functionality."""
    print("=== Nalo Solutions USSD API Demo ===\\n")

    # Initialize USSD application
    ussd_app = MyUSSDApplication()

    # Example 1: Initial USSD dial
    print("1. Initial USSD Request (User dials *920#):")
    initial_request = {
        "USERID": "NALOTest",
        "MSISDN": "233501234567",
        "USERDATA": "",
        "MSGTYPE": True,
        "SESSIONID": "16590115252429751",
        "NETWORK": "MTN",
    }

    response = ussd_app.handle_ussd_request(initial_request)
    print(f"Request: {initial_request}")
    print(f"Response: {response}")
    print()

    # Example 2: User selects option 1 (Check Balance)
    print("2. User selects option 1 (Check Balance):")
    continuing_request = {
        "USERID": "NALOTest",
        "MSISDN": "233501234567",
        "USERDATA": "1",
        "MSGTYPE": False,
        "SESSIONID": "16590115252429751",
        "NETWORK": "MTN",
    }

    response = ussd_app.handle_ussd_request(continuing_request)
    print(f"Request: {continuing_request}")
    print(f"Response: {response}")
    print()

    # Example 3: User continues after balance check
    print("3. User continues after balance check:")
    continue_request = {
        "USERID": "NALOTest",
        "MSISDN": "233501234567",
        "USERDATA": "1",
        "MSGTYPE": False,
        "SESSIONID": "16590115252429751",
        "NETWORK": "MTN",
    }

    response = ussd_app.handle_ussd_request(continue_request)
    print(f"Request: {continue_request}")
    print(f"Response: {response}")
    print()

    # Example 4: Using NaloSolutionsClient utilities
    print("4. Using NaloSolutionsClient USSD utilities:")
    client = NaloSolutionsClient()

    # Create a menu
    menu = client.create_ussd_menu(
        title="Bank Services",
        options={"1": "Balance", "2": "Transfer", "0": "Exit"},
        userid="NALOTest",
        msisdn="233501234567",
    )
    print(f"Menu: {menu}")

    # Create a response message
    response_msg = client.create_ussd_response(
        message="Transaction completed successfully!",
        userid="NALOTest",
        msisdn="233501234567",
        continue_session=False,
    )
    print(f"Response: {response_msg}")
    print()

    print("=== USSD Demo Complete ===")
    print("\\nTo run the Flask webhook:")
    print("1. Install Flask: pip install flask")
    print("2. Set your endpoint URL in Nalo dashboard")
    print("3. Run: python ussd_comprehensive_demo.py")


if __name__ == "__main__":
    main()

    # Optionally start Flask webhook server
    flask_app = create_ussd_webhook_app()
    if flask_app:
        print("\\nStarting Flask USSD webhook server...")
        print("Webhook endpoint: http://localhost:5000/ussd-webhook")
        print("Health check: http://localhost:5000/health")
        flask_app.run(debug=True, port=5000)
