"""
Simple implementation of NaloSolutions for testing.
"""

import requests
import hashlib
from typing import Dict, Any, Optional, List, Literal, Union
from urllib.parse import urlencode


class NaloSolutions:
    """Client for interacting with Nalo Solutions APIs (Payments, SMS, USSD, Email)."""

    def __init__(self, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        Initialize Nalo Solutions client.

        Args:
            config: Configuration dictionary with service settings
            **kwargs: Alternative way to pass individual parameters
        """
        # Initialize session management for USSD
        self._ussd_sessions = {}

        # Handle both config dict and individual parameters
        if config is not None:
            self.config = config
            self._init_from_config(config)
        else:
            self._init_from_kwargs(kwargs)

        # Initialize HTTP session
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Content-Type": "application/json",
                "User-Agent": "Nunyakata-Python-Client/0.1.0",
            }
        )

    def _init_from_config(self, config: Dict[str, Any]):
        """Initialize from configuration dictionary."""
        # Payment configuration
        payment_config = config.get("payment", {})
        self.payment_merchant_id = payment_config.get("merchant_id")
        self.payment_username = payment_config.get("username")
        self.payment_password = payment_config.get("password")
        self.payment_environment = payment_config.get("environment", "production")

        # SMS configuration
        sms_config = config.get("sms", {})
        self.sms_username = sms_config.get("username")
        self.sms_password = sms_config.get("password")
        self.sms_auth_key = sms_config.get("auth_key")
        self.sms_sender_id = sms_config.get("sender_id", "DEFAULT")

        # USSD configuration
        ussd_config = config.get("ussd", {})
        self.ussd_userid = ussd_config.get("userid")
        self.ussd_msisdn = ussd_config.get("msisdn")
        self.ussd_environment = ussd_config.get("environment", "sandbox")

        # Email configuration
        email_config = config.get("email", {})
        self.email_username = email_config.get("username")
        self.email_password = email_config.get("password")
        self.email_auth_key = email_config.get("auth_key")
        self.email_from_email = email_config.get("from_email")
        self.email_from_name = email_config.get("from_name")

        # Set API URLs based on environment
        self._set_api_urls()

    def _init_from_kwargs(self, kwargs):
        """Initialize from keyword arguments."""
        # Initialize empty config for URL setting
        self.config = {}

        # Payment parameters
        self.payment_merchant_id = kwargs.get("payment_merchant_id")
        self.payment_username = kwargs.get("payment_username")
        self.payment_password = kwargs.get("payment_password")
        self.payment_environment = kwargs.get("payment_environment", "production")

        # SMS parameters
        self.sms_username = kwargs.get("sms_username")
        self.sms_password = kwargs.get("sms_password")
        self.sms_auth_key = kwargs.get("sms_auth_key")
        self.sms_sender_id = kwargs.get("sms_sender_id", "DEFAULT")

        # USSD parameters
        self.ussd_userid = kwargs.get("ussd_userid")
        self.ussd_msisdn = kwargs.get("ussd_msisdn")
        self.ussd_environment = kwargs.get("ussd_environment", "sandbox")

        # Email parameters
        self.email_username = kwargs.get("email_username")
        self.email_password = kwargs.get("email_password")
        self.email_auth_key = kwargs.get("email_auth_key")
        self.email_from_email = kwargs.get("email_from_email")
        self.email_from_name = kwargs.get("email_from_name")

        # Set API URLs
        self._set_api_urls()

    def _set_api_urls(self):
        """Set API URLs based on environment."""
        # Payment API - always uses production endpoint according to docs
        self.payment_base_url = "https://api.nalosolutions.com/payplus/api"

        # SMS and Email APIs - using correct defaults from API documentation
        base_url = self.config.get("sms", {}).get(
            "base_url", "https://sms.nalosolutions.com"
        )
        # GET method uses /send-message/, POST uses /send-message/ (same endpoint with trailing slash)
        self.sms_base_url_get = (
            f"{base_url}/smsbackend/clientapi/Resl_Nalo/send-message"
        )
        self.sms_base_url_post = f"{base_url}/smsbackend/Resl_Nalo/send-message/"
        # Email API uses the same base but different endpoint
        self.email_base_url = f"{base_url}/smsbackend/clientapi/Nal_resl/send-email/"

    def _make_request(self, method: str, url: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request and handle response."""
        try:
            response = self.session.request(method, url, **kwargs)

            # For successful responses, try to return JSON
            if response.status_code < 400:
                try:
                    return response.json()
                except ValueError:
                    # If JSON parsing fails, return the raw text response
                    return {
                        "status": "success",
                        "message": "Response received",
                        "raw_response": response.text.strip(),
                        "status_code": response.status_code,
                    }

            # For error responses, try to get the JSON error message
            try:
                error_data = response.json()
                return error_data
            except ValueError:
                # If JSON parsing fails, create a response with the raw text
                return {
                    "status": "error",
                    "message": f"Request failed: {response.status_code} {response.reason}",
                    "raw_response": response.text.strip(),
                    "status_code": response.status_code,
                }

        except requests.exceptions.Timeout:
            return {"status": "error", "message": "Request timeout"}
        except requests.exceptions.ConnectionError:
            return {"status": "error", "message": "Network connection error"}
        except requests.exceptions.RequestException as e:
            return {"status": "error", "message": f"Request failed: {str(e)}"}
        except Exception as e:
            return {"status": "error", "message": f"Unexpected error: {str(e)}"}

    # === PAYMENT SERVICES ===

    def make_payment(
        self,
        amount: float,
        customer_number: str,
        customer_name: str,
        item_desc: str,
        order_id: str,
        payby: Literal["MTN", "AIRTELTIGO", "VODAFONE"],
        callback_url: str,
        new_voda_payment: bool = False,
        is_ussd: bool = False,
    ) -> Dict[str, Any]:
        """
        Process a mobile money payment using Nalo PayPlus API.

        Args:
            amount: Payment amount in GHS
            customer_number: Customer phone number in format 233xxxxxxxxx
            customer_name: Name of the payment authorizer
            item_desc: Description of purchased item/service
            order_id: Unique payment order ID
            payby: Network operator (MTN, AIRTELTIGO, VODAFONE)
            callback_url: URL to receive payment status callbacks
            new_voda_payment: Use new Vodafone USSD payment (Vodafone only)
            is_ussd: Whether request is from NALO USSD extension

        Returns:
            Payment response dictionary
        """
        # Validate inputs
        if not amount or amount <= 0:
            raise ValueError("Amount must be greater than 0")
        if not customer_number:
            raise ValueError("Customer number must be provided")
        if not customer_name:
            raise ValueError("Customer name must be provided")
        if not item_desc:
            raise ValueError("Item description must be provided")
        if not order_id:
            raise ValueError("Order ID must be provided")
        if payby not in ["MTN", "AIRTELTIGO", "VODAFONE"]:
            raise ValueError("payby must be one of: MTN, AIRTELTIGO, VODAFONE")
        if not callback_url:
            raise ValueError("Callback URL must be provided")

        # Check authentication
        if not (
            self.payment_merchant_id and self.payment_username and self.payment_password
        ):
            raise ValueError(
                "Payment credentials (merchant_id, username, password) must be provided"
            )

        # Generate random 4-digit key
        import random

        key = f"{random.randint(1000, 9999)}"

        # Generate secret according to API docs: md5(username + key + md5(password))
        password_hash = hashlib.md5(self.payment_password.encode()).hexdigest()
        secret_string = f"{self.payment_username}{key}{password_hash}"
        secret = hashlib.md5(secret_string.encode()).hexdigest()

        # Prepare payment data according to API documentation
        payment_data = {
            "merchant_id": self.payment_merchant_id,
            "key": key,
            "secrete": secret,  # Note: API uses 'secrete' not 'secret'
            "order_id": order_id,
            "customerName": customer_name,
            "amount": str(amount),  # API expects string
            "item_desc": item_desc,
            "customerNumber": customer_number,
            "callback": callback_url,
            "payby": payby,
        }

        # Add optional parameters
        if new_voda_payment and payby == "VODAFONE":
            payment_data["newVodaPayment"] = True
        if is_ussd:
            payment_data["isussd"] = 1

        # Make payment request
        return self._make_request("POST", self.payment_base_url, json=payment_data)

    def make_simple_payment(
        self,
        amount: float,
        phone_number: str,
        customer_name: str,
        description: str,
        callback_url: str,
        network: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Simplified payment method with automatic network detection and order ID generation.

        Args:
            amount: Payment amount in GHS
            phone_number: Customer phone number (233xxxxxxxxx format)
            customer_name: Name of the customer
            description: Description of the payment
            callback_url: URL to receive payment callbacks
            network: Network operator (auto-detected if not provided)

        Returns:
            Payment response dictionary
        """
        import uuid
        import time

        # Auto-detect network if not provided
        if not network:
            if (
                phone_number.startswith("233024")
                or phone_number.startswith("233054")
                or phone_number.startswith("233055")
            ):
                network = "MTN"
            elif phone_number.startswith("233020") or phone_number.startswith("233050"):
                network = "VODAFONE"
            elif (
                phone_number.startswith("233027")
                or phone_number.startswith("233057")
                or phone_number.startswith("233026")
                or phone_number.startswith("233056")
            ):
                network = "AIRTELTIGO"
            else:
                network = "MTN"  # Default to MTN

        # Generate unique order ID
        order_id = f"ORDER_{int(time.time())}_{str(uuid.uuid4())[:8]}"

        return self.make_payment(
            amount=amount,
            customer_number=phone_number,
            customer_name=customer_name,
            item_desc=description,
            order_id=order_id,
            payby=network,  # type: ignore
            callback_url=callback_url,
        )

    def handle_payment_callback(self, callback_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle payment callback from Nalo PayPlus API.

        Args:
            callback_data: Callback data received from Nalo

        Returns:
            Standard callback response
        """
        # Validate callback data
        required_fields = ["Timestamp", "Status", "InvoiceNo", "Order_id"]
        if not all(field in callback_data for field in required_fields):
            return {"Response": "ERROR", "message": "Invalid callback data"}

        # Process the callback (you can add custom logic here)
        status = callback_data.get("Status", "").upper()
        if status in ["PAID", "ACCEPTED"]:
            # Payment successful - add your business logic here
            pass
        elif status == "FAILED":
            # Payment failed - add your business logic here
            pass

        # Return standard callback response
        return {"Response": "OK"}

    # === SMS SERVICES ===

    def send_sms(
        self,
        phone_number: str,
        message: str,
        method: Literal["GET", "POST"] = "GET",
        sender_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Send SMS message.

        Args:
            phone_number: Recipient phone number
            message: SMS message content
            method: HTTP method to use (GET or POST)
            sender_id: Custom sender ID

        Returns:
            SMS response dictionary
        """
        # Validate inputs
        if not phone_number:
            raise ValueError("Phone number must be provided")
        if not message:
            raise ValueError("Message must be provided")
        if method not in ["GET", "POST"]:
            raise ValueError("Method must be 'GET' or 'POST'")
        if len(message) > 1000:
            raise ValueError("Message is too long")

        # Check authentication
        if not ((self.sms_username and self.sms_password) or self.sms_auth_key):
            raise ValueError("Authentication credentials must be provided")

        if method == "GET":
            # GET method - prepare SMS data according to actual API documentation
            sms_data = {
                "destination": phone_number,
                "message": message,
                "source": sender_id or self.sms_sender_id,
                "type": "0",  # 0 for text messages
                "dlr": "1",  # 1 for delivery reports
            }

            # Add authentication for GET
            if self.sms_auth_key:
                sms_data["key"] = self.sms_auth_key
            else:
                sms_data["username"] = self.sms_username
                sms_data["password"] = self.sms_password

            # Send as query parameters
            url = f"{self.sms_base_url_get}?" + urlencode(sms_data)
            response = self._make_request("GET", url)

            # Parse GET response format: "1701|233265542141|api.0039013.20250127.1753576627.8301058"
            if response.get("status") == "success" and "raw_response" in response:
                parts = response["raw_response"].split("|")
                if len(parts) >= 3:
                    return {
                        "status": "success",
                        "message": "SMS sent successfully",
                        "code": parts[0],
                        "phone_number": parts[1],
                        "message_id": parts[2],
                        "raw_response": response["raw_response"],
                    }
                else:
                    return {
                        "status": "success",
                        "message": "SMS sent successfully",
                        "raw_response": response["raw_response"],
                    }
            return response
        else:
            # POST method - different parameter names according to API docs
            sms_data = {
                "msisdn": phone_number,  # POST uses 'msisdn' not 'destination'
                "message": message,
                "sender_id": sender_id
                or self.sms_sender_id,  # POST uses 'sender_id' not 'source'
            }

            # Add authentication for POST
            if self.sms_auth_key:
                sms_data["key"] = self.sms_auth_key
            else:
                sms_data["username"] = self.sms_username
                sms_data["password"] = self.sms_password

            # Send as raw JSON string for POST (as shown in API docs)
            import json

            json_payload = json.dumps(sms_data)
            headers = {"Content-Type": "application/json"}
            response = self._make_request(
                "POST", self.sms_base_url_post, data=json_payload, headers=headers
            )

            # Parse POST JSON response format: {"status": "1701", "job_id": "api.0000011.20221222.0000003", "msisdn": "233244071872"}
            if response.get("status") == "success" and "raw_response" in response:
                try:
                    import json

                    json_response = json.loads(response["raw_response"])
                    return {
                        "status": "success",
                        "message": "SMS sent successfully",
                        "code": json_response.get("status"),
                        "phone_number": json_response.get("msisdn"),
                        "message_id": json_response.get("job_id"),
                        "raw_response": response["raw_response"],
                    }
                except (json.JSONDecodeError, KeyError):
                    return {
                        "status": "success",
                        "message": "SMS sent successfully",
                        "raw_response": response["raw_response"],
                    }
            elif response.get("status") and response.get("job_id"):
                # Direct JSON response
                return {
                    "status": "success",
                    "message": "SMS sent successfully",
                    "code": response.get("status"),
                    "phone_number": response.get("msisdn"),
                    "message_id": response.get("job_id"),
                    "raw_response": str(response),
                }
            return response

    # === USSD SERVICES ===

    def handle_ussd_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle USSD session request according to Nalo USSD API format.

        Expected request format:
        {
            "USERID": "NALOTest",
            "MSISDN": "233XXXXXXXXX",
            "USERDATA": "user_input",
            "MSGTYPE": true/false,  # true=initial, false=subsequent
            "NETWORK": "MTN/VODAFONE/AIRTELTIGO",
            "SESSIONID": "unique_session_id"
        }

        Args:
            request_data: USSD request data from Nalo API

        Returns:
            USSD response dictionary in Nalo format
        """
        try:
            # Extract required parameters according to Nalo API documentation
            userid = request_data.get("USERID", "")
            msisdn = request_data.get("MSISDN", "")
            userdata = request_data.get("USERDATA", "")
            msgtype = request_data.get("MSGTYPE", True)
            network = request_data.get("NETWORK", "")
            sessionid = request_data.get("SESSIONID", "")

            # Validate required parameters
            if not userid:
                return self._create_nalo_ussd_response(
                    userid, msisdn, userdata, "Invalid USERID", False
                )

            if not sessionid:
                return self._create_nalo_ussd_response(
                    userid, msisdn, userdata, "Session error occurred", False
                )

            # Check if this is an initial dial (MSGTYPE = true)
            if msgtype:
                # Initial dial - create new session
                self._init_ussd_session(sessionid)
                return self._handle_initial_ussd_request(
                    userid, msisdn, userdata, network, sessionid
                )
            else:
                # Subsequent dial - handle based on session state
                return self._handle_subsequent_ussd_request(
                    userid, msisdn, userdata, network, sessionid
                )

        except Exception:
            # Handle any unexpected errors
            return self._create_nalo_ussd_response(
                request_data.get("USERID", ""),
                request_data.get("MSISDN", ""),
                request_data.get("USERDATA", ""),
                "Technical difficulties encountered. Please try again.",
                False,
            )

    def _handle_initial_ussd_request(
        self, userid: str, msisdn: str, userdata: str, network: str, sessionid: str
    ) -> Dict[str, Any]:
        """Handle initial USSD request (MSGTYPE = true)."""
        # Create welcome menu - this is a generic demo menu
        welcome_msg = (
            "Welcome to USSD Demo\n"
            "Choose an option:\n"
            "1. Check Balance\n"
            "2. Account Info\n"
            "3. Services\n"
            "4. Settings\n"
            "0. Help"
        )

        # Update session with initial state
        self.update_ussd_session(
            sessionid,
            {"stage": 0, "msisdn": msisdn, "network": network, "userid": userid},
        )

        return self._create_nalo_ussd_response(
            userid, msisdn, userdata, welcome_msg, True
        )

    def _handle_subsequent_ussd_request(
        self, userid: str, msisdn: str, userdata: str, network: str, sessionid: str
    ) -> Dict[str, Any]:
        """Handle subsequent USSD requests (MSGTYPE = false)."""
        # Get current session
        session = self.get_ussd_session(sessionid)
        current_stage = session.get("stage", 0)

        if current_stage == 0:
            # Main menu selection
            return self._handle_main_menu_selection(
                userid, msisdn, userdata, network, sessionid
            )
        elif current_stage == 1:
            # Sub-menu handling - delegate to generic service handler
            service = session.get("data", {}).get("service", "")
            return self._handle_service_menu(
                userid, msisdn, userdata, network, sessionid, service
            )
        elif current_stage == 2:
            # Final processing - generic demo response
            msg = (
                "Transaction processed successfully!\nThank you for using our service."
            )
            self.clear_ussd_session(sessionid)
            return self._create_nalo_ussd_response(userid, msisdn, userdata, msg, False)
        else:
            # Invalid stage - reset session
            self.clear_ussd_session(sessionid)
            return self._create_nalo_ussd_response(
                userid, msisdn, userdata, "Session expired. Please try again.", False
            )

    def _handle_service_menu(
        self,
        userid: str,
        msisdn: str,
        userdata: str,
        network: str,
        sessionid: str,
        service: str,
    ) -> Dict[str, Any]:
        """Handle specific service menu selections - to be overridden by user implementations."""
        # This is a generic handler that users can override for their specific business logic
        if service == "services":
            try:
                selection = int(userdata.strip())
                if selection == 1:
                    msg = "Service A selected\nThis is a demo response.\nOverride this method for custom logic."
                elif selection == 2:
                    msg = "Service B selected\nThis is a demo response.\nOverride this method for custom logic."
                elif selection == 3:
                    msg = "Service C selected\nThis is a demo response.\nOverride this method for custom logic."
                else:
                    msg = "Invalid selection. Please choose 1-3."
                return self._create_nalo_ussd_response(
                    userid, msisdn, userdata, msg, False
                )
            except ValueError:
                msg = "Invalid input. Please enter a valid number."
                return self._create_nalo_ussd_response(
                    userid, msisdn, userdata, msg, False
                )
        else:
            msg = f"Service '{service}' selected.\nThis is a demo implementation.\nOverride this method for custom logic."
            return self._create_nalo_ussd_response(userid, msisdn, userdata, msg, False)

    def _handle_main_menu_selection(
        self, userid: str, msisdn: str, userdata: str, network: str, sessionid: str
    ) -> Dict[str, Any]:
        """Handle main menu selection."""
        try:
            selection = int(userdata.strip())

            if selection == 1:
                # Check Balance - demo response
                msg = "Demo Balance: GHS 150.75\nThank you for using our service!"
                return self._create_nalo_ussd_response(
                    userid, msisdn, userdata, msg, False
                )

            elif selection == 2:
                # Account Info - demo response
                msg = f"Account Information\nPhone: {msisdn}\nNetwork: {network}\nStatus: Active"
                return self._create_nalo_ussd_response(
                    userid, msisdn, userdata, msg, False
                )

            elif selection == 3:
                # Services - generic sub-menu
                msg = (
                    "Available Services\n"
                    "1. Service A\n"
                    "2. Service B\n"
                    "3. Service C"
                )
                self.update_ussd_session(sessionid, {"stage": 1, "service": "services"})
                return self._create_nalo_ussd_response(
                    userid, msisdn, userdata, msg, True
                )

            elif selection == 4:
                # Settings - demo response
                msg = "Settings\nLanguage: English\nNotifications: Enabled\nAccount Type: Standard"
                return self._create_nalo_ussd_response(
                    userid, msisdn, userdata, msg, False
                )

            elif selection == 0:
                # Help
                msg = (
                    "Help & Support\n"
                    "This is a demo USSD implementation.\n"
                    "Override the methods to add your business logic.\n"
                    "Thank you!"
                )
                return self._create_nalo_ussd_response(
                    userid, msisdn, userdata, msg, False
                )

            else:
                msg = "Invalid selection. Please choose 0-4."
                return self._create_nalo_ussd_response(
                    userid, msisdn, userdata, msg, False
                )

        except ValueError:
            msg = "Invalid input. Please enter a number (0-4)."
            return self._create_nalo_ussd_response(userid, msisdn, userdata, msg, False)

    def _create_nalo_ussd_response(
        self,
        userid: str,
        msisdn: str,
        userdata: str,
        message: str,
        continue_session: bool,
    ) -> Dict[str, Any]:
        """
        Create USSD response in Nalo API format.

        Args:
            userid: The USERID from the request
            msisdn: The MSISDN from the request
            userdata: The USERDATA from the request
            message: Message to display to user
            continue_session: Whether to continue the session (true) or end it (false)

        Returns:
            Response dictionary in Nalo format
        """
        return {
            "USERID": userid,
            "MSISDN": msisdn,
            "USERDATA": userdata,
            "MSG": message,
            "MSGTYPE": continue_session,
        }

    def _init_ussd_session(self, sessionid: str):
        """Initialize a new USSD session."""
        self._ussd_sessions[sessionid] = {
            "stage": 0,
            "data": {},
            "created_at": self._get_current_timestamp(),
        }

    def _get_current_timestamp(self) -> str:
        """Get current timestamp."""
        import datetime

        return datetime.datetime.now().isoformat()

    def create_ussd_menu(
        self, title: str, options: List[str], footer: Optional[str] = None
    ) -> str:
        """Create a USSD menu."""
        menu = f"{title}\\n"
        for i, option in enumerate(options, 1):
            menu += f"{i}. {option}\\n"
        if footer:
            menu += f"\\n{footer}"
        return menu

    def create_ussd_response(
        self,
        message: str,
        continue_session: bool = True,
        sessionid: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a USSD response."""
        response = {
            "response": "CON" if continue_session else "END",
            "message": message,
        }
        if sessionid:
            response["sessionid"] = sessionid
        return response

    def get_ussd_session(self, sessionid: str) -> Dict[str, Any]:
        """Get or create USSD session."""
        if sessionid not in self._ussd_sessions:
            self._ussd_sessions[sessionid] = {"step": 0, "data": {}}
        return self._ussd_sessions[sessionid]

    def update_ussd_session(self, sessionid: str, data: Dict[str, Any]):
        """Update USSD session data."""
        if sessionid in self._ussd_sessions:
            session = self._ussd_sessions[sessionid]
            for key, value in data.items():
                if key in ["step", "stage"]:
                    # Stage/step goes at the top level
                    session["stage"] = value
                else:
                    # Other data goes into the data sub-object
                    if "data" not in session:
                        session["data"] = {}
                    session["data"][key] = value

    def clear_ussd_session(self, sessionid: str):
        """Clear USSD session."""
        if sessionid in self._ussd_sessions:
            del self._ussd_sessions[sessionid]

    def validate_ussd_input(self, input_value: str, valid_options: List[str]) -> bool:
        """Validate USSD input."""
        return input_value in valid_options

    def validate_phone_number(self, phone_number: str) -> bool:
        """Validate phone number format."""
        if not phone_number:
            return False
        # Remove non-digits
        digits = "".join(filter(str.isdigit, phone_number))
        # Ghana numbers should be 10 digits (without country code) or 12 digits (with country code)
        # Check for valid Ghana number patterns
        if len(digits) == 10:
            # Must start with 0 (local format)
            return digits.startswith("0")
        elif len(digits) == 12:
            # Must start with 233 (country code)
            return digits.startswith("233")
        else:
            return False

    def validate_amount(self, amount_str: str) -> bool:
        """Validate amount format."""
        try:
            amount = float(amount_str)
            # Check if amount is positive and has at most 2 decimal places
            if amount <= 0:
                return False
            # Check decimal places
            if "." in amount_str:
                decimal_part = amount_str.split(".")[1]
                return len(decimal_part) <= 2
            return True
        except ValueError:
            return False

    # === EMAIL SERVICES ===

    def send_email(
        self,
        to_email: Union[str, List[str]],
        subject: str,
        message: str,
        from_email: Optional[str] = None,
        sender_name: Optional[str] = None,
        callback_url: Optional[str] = None,
        template: Optional[str] = None,
        html: Optional[str] = None,
        attachments: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Send email message using Nalo Email API.

        Args:
            to_email: Recipient email address(es) - can be string or list
            subject: Email subject
            message: Email message content
            from_email: Sender email address (must be verified)
            sender_name: Name of the sender
            callback_url: Callback URL for delivery status
            template: Template name for Nalo's cloud platform
            html: Encoded HTML content
            attachments: List of attachment file paths

        Returns:
            Email response dictionary
        """
        # Validate inputs
        if not to_email:
            raise ValueError("To email must be provided")
        if not subject:
            raise ValueError("Subject must be provided")
        if not message:
            raise ValueError("Message must be provided")

        # Validate email addresses
        if isinstance(to_email, str):
            if not self.validate_email(to_email):
                raise ValueError("Invalid email address format")
            email_to = [to_email]
        else:
            for email in to_email:
                if not self.validate_email(email):
                    raise ValueError(f"Invalid email address format: {email}")
            email_to = to_email

        # Check authentication
        if not ((self.email_username and self.email_password) or self.email_auth_key):
            raise ValueError("Authentication credentials must be provided")

        # Prepare email data according to API documentation
        email_data = {
            "emailTo": email_to,
            "subject": subject,
            "emailBody": message,
            "emailFrom": from_email or self.email_from_email,
            "senderName": sender_name or self.email_from_name or "API User",
        }

        # Add authentication
        if self.email_auth_key:
            email_data["key"] = self.email_auth_key
        else:
            email_data["username"] = self.email_username
            email_data["password"] = self.email_password

        # Add optional fields
        if callback_url:
            email_data["callBackUrl"] = callback_url
        if template:
            email_data["template"] = template
        if html:
            email_data["html"] = html

        # Handle attachments
        if attachments:
            return self._send_email_with_attachments(email_data, attachments)
        else:
            # Send as JSON for simple emails
            return self._make_request("POST", self.email_base_url, json=email_data)

    def _send_email_with_attachments(
        self, email_data: Dict[str, Any], attachments: List[str]
    ) -> Dict[str, Any]:
        """Send email with file attachments using form data."""
        files = {}

        # Process attachments
        for i, attachment_path in enumerate(attachments):
            try:
                with open(attachment_path, "rb") as f:
                    files["attach_file"] = f.read()
            except FileNotFoundError:
                raise ValueError(f"Attachment file not found: {attachment_path}")

        # Convert email_data for form submission
        form_data = email_data.copy()

        # Convert emailTo list to individual fields for form data
        if isinstance(form_data.get("emailTo"), list):
            if len(form_data["emailTo"]) == 1:
                form_data["emailTo"] = form_data["emailTo"][0]
            else:
                # For multiple recipients in form data, use comma-separated string
                form_data["emailTo"] = ",".join(form_data["emailTo"])

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
        }

        return self._make_request(
            "POST",
            self.email_base_url,
            data=form_data,
            files=files,
            headers=headers,
        )

    def send_html_email(
        self,
        to_email: Union[str, List[str]],
        subject: str,
        html_content: str,
        from_email: Optional[str] = None,
        sender_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Send HTML email using the html parameter."""
        return self.send_email(
            to_email=to_email,
            subject=subject,
            message="HTML Email",  # Provide a default message when using HTML
            from_email=from_email,
            sender_name=sender_name,
            html=html_content,
        )

    def send_bulk_email(
        self,
        recipients: List[str],
        subject: str,
        message: str,
        from_email: Optional[str] = None,
        sender_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Send bulk emails to multiple recipients in a single API call."""
        return self.send_email(
            to_email=recipients,
            subject=subject,
            message=message,
            from_email=from_email,
            sender_name=sender_name,
        )

    def send_email_with_template(
        self,
        to_email: Union[str, List[str]],
        template_name: str,
        content: str,
        subject: str,
        from_email: Optional[str] = None,
        sender_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Send email using Nalo's cloud template with placeholder {{{content}}}."""
        return self.send_email(
            to_email=to_email,
            subject=subject,
            message=content,  # This will be inserted into the template's {{{content}}} placeholder
            from_email=from_email,
            sender_name=sender_name,
            template=template_name,
        )

    def validate_email(self, email: str) -> bool:
        """Validate email address format."""
        if not email or "@" not in email:
            return False

        # Check for spaces or invalid characters
        if " " in email or not email.strip():
            return False

        parts = email.split("@")
        if len(parts) != 2:
            return False

        local, domain = parts
        # Basic validation - local and domain parts must exist and not be empty
        if not local.strip() or not domain.strip():
            return False

        # Domain must contain at least one dot
        if "." not in domain:
            return False

        return True

    def handle_email_callback(self, callback_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle email delivery callback from Nalo Email API.

        Expected callback parameters:
        - mid: unique id for the email
        - sender_address: sender email address
        - destination_address: recipient address
        - timestamp: date and time mail was sent
        - status_desc: the state of that particular email job

        Args:
            callback_data: Callback data received from Nalo

        Returns:
            Processed callback response
        """
        if "mid" in callback_data and "status_desc" in callback_data:
            return {
                "processed": True,
                "email_id": callback_data["mid"],
                "sender": callback_data.get("sender_address"),
                "recipient": callback_data.get("destination_address"),
                "timestamp": callback_data.get("timestamp"),
                "status": callback_data["status_desc"],
            }
        else:
            return {"processed": False, "error": "Invalid callback data"}

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        if hasattr(self, "session"):
            self.session.close()


# Backward compatibility alias
NaloSolutionsClient = NaloSolutions
