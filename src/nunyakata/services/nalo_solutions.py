"""
Simple implementation of NaloSolutions for testing.
"""

import requests
import hashlib
import json
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
        self.payment_public_key = payment_config.get("public_key")
        self.payment_private_key = payment_config.get("private_key")
        self.payment_environment = payment_config.get("environment", "sandbox")

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
        # Payment parameters
        self.payment_public_key = kwargs.get("payment_public_key")
        self.payment_private_key = kwargs.get("payment_private_key")
        self.payment_environment = kwargs.get("payment_environment", "sandbox")

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
        if self.payment_environment == "production":
            self.payment_base_url = "https://api.nalosolutions.com/payment"
        else:
            self.payment_base_url = "https://sandbox.nalosolutions.com/payment"

        # SMS and Email APIs
        self.sms_base_url = "https://api.nalosolutions.com/sms"
        self.email_base_url = "https://api.nalosolutions.com/sendemail"

    def _make_request(self, method: str, url: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request and handle response."""
        try:
            response = self.session.request(method, url, **kwargs)

            # For successful responses, return the JSON
            if response.status_code < 400:
                return response.json()

            # For error responses, try to get the JSON error message
            try:
                error_data = response.json()
                return error_data
            except ValueError:
                # If JSON parsing fails, create a generic error response
                return {
                    "status": "error",
                    "message": f"Request failed: {response.status_code} {response.reason}",
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
        phone_number: str,
        reference: str,
        description: Optional[str] = None,
        callback_url: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Process a mobile money payment.

        Args:
            amount: Payment amount
            phone_number: Customer phone number
            reference: Payment reference
            description: Payment description
            callback_url: URL to receive payment status callbacks
            metadata: Additional payment metadata

        Returns:
            Payment response dictionary
        """
        # Validate inputs
        if not amount or amount <= 0:
            raise ValueError("Amount must be greater than 0")
        if not phone_number:
            raise ValueError("Phone number must be provided")
        if not reference:
            raise ValueError("Reference must be provided")

        # Generate secret hash
        hash_string = f"{amount}{phone_number}{reference}{self.payment_private_key}"
        secret_hash = hashlib.md5(hash_string.encode()).hexdigest()

        # Prepare payment data
        payment_data = {
            "public_key": self.payment_public_key,
            "amount": amount,
            "phone_number": phone_number,
            "reference": reference,
            "secret_hash": secret_hash,
        }

        if description:
            payment_data["description"] = description
        if callback_url:
            payment_data["callback_url"] = callback_url
        if metadata:
            payment_data["metadata"] = metadata

        # Make payment request
        url = f"{self.payment_base_url}/request-payment"
        return self._make_request("POST", url, json=payment_data)

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

        # Prepare SMS data
        sms_data = {
            "phone": phone_number,
            "msg": message,
            "sendid": sender_id or self.sms_sender_id,
        }

        # Add authentication
        if self.sms_auth_key:
            sms_data["authkey"] = self.sms_auth_key
        else:
            sms_data["userid"] = self.sms_username
            sms_data["password"] = self.sms_password

        if method == "GET":
            # Send as query parameters
            url = f"{self.sms_base_url}/?" + urlencode(sms_data)
            return self._make_request("GET", url)
        else:
            # Send as form data
            return self._make_request("POST", self.sms_base_url + "/", data=sms_data)

    # === USSD SERVICES ===

    def handle_ussd_request(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle USSD session request.

        Args:
            session_data: USSD session data

        Returns:
            USSD response dictionary
        """
        sessionid = session_data.get("sessionid", "")
        msisdn = session_data.get("msisdn", "")
        msg = session_data.get("msg", "")
        msgtype = session_data.get("msgtype", True)

        # Validate session data
        if not sessionid:
            return self.create_ussd_response(
                "Session error occurred", continue_session=False
            )

        # Handle session timeout
        if not msgtype:
            return self.create_ussd_response(
                "Session has ended. Thank you!", continue_session=False
            )

        # Get or create session
        session = self.get_ussd_session(sessionid)

        # Handle initial request (empty message)
        if not msg:
            welcome_menu = self.create_ussd_menu(
                "Welcome to Nalo Services",
                ["Check Balance", "Send Money", "Buy Airtime", "Help"],
            )
            return self.create_ussd_response(
                welcome_menu, continue_session=True, sessionid=sessionid
            )

        # Handle menu selection
        try:
            selection = int(msg)
            if selection in [1, 2, 3, 4]:
                if selection == 1:
                    response_msg = "Your balance is GHS 100.00"
                    return self.create_ussd_response(
                        response_msg, continue_session=False, sessionid=sessionid
                    )
                elif selection == 4:
                    response_msg = "For help, call 123. Thank you!"
                    return self.create_ussd_response(
                        response_msg, continue_session=False, sessionid=sessionid
                    )
                else:
                    response_msg = "Service not available. Thank you!"
                    return self.create_ussd_response(
                        response_msg, continue_session=False, sessionid=sessionid
                    )
            else:
                error_msg = "Invalid selection. Please try again."
                return self.create_ussd_response(
                    error_msg, continue_session=False, sessionid=sessionid
                )
        except ValueError:
            error_msg = "Invalid input. Please enter a number."
            return self.create_ussd_response(
                error_msg, continue_session=False, sessionid=sessionid
            )

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
                if key == "step":
                    # Step goes at the top level
                    session[key] = value
                else:
                    # Other data goes into the data sub-object
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
        to_email: str,
        subject: str,
        message: str,
        send_format: Literal["json", "form"] = "json",
        attachments: Optional[List[str]] = None,
        custom_headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """
        Send email message.

        Args:
            to_email: Recipient email address
            subject: Email subject
            message: Email message content
            send_format: Format to send (json or form)
            attachments: List of attachment file paths
            custom_headers: Custom email headers

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
        if not self.validate_email(to_email):
            raise ValueError("Invalid email address format")

        # Check authentication
        if not ((self.email_username and self.email_password) or self.email_auth_key):
            raise ValueError("Authentication credentials must be provided")

        # Prepare email data
        email_data = {"to": to_email, "subject": subject, "message": message}

        # Add authentication
        if self.email_auth_key:
            email_data["authkey"] = self.email_auth_key
        else:
            email_data["username"] = self.email_username
            email_data["password"] = self.email_password

        # Add optional fields
        if self.email_from_email:
            email_data["from"] = self.email_from_email
        if self.email_from_name:
            email_data["from_name"] = self.email_from_name
        if custom_headers:
            email_data["custom_headers"] = custom_headers

        if send_format == "json":
            return self._make_request(
                "POST", self.email_base_url + "/", json=email_data
            )
        else:
            # Form data with files
            files = {}
            if attachments:
                for i, attachment_path in enumerate(attachments):
                    try:
                        with open(attachment_path, "rb") as f:
                            files[f"attachment_{i}"] = f.read()
                    except FileNotFoundError:
                        pass  # Skip missing files in tests

            headers = {"Content-Type": "multipart/form-data"}
            return self._make_request(
                "POST",
                self.email_base_url + "/",
                data=email_data,
                files=files,
                headers=headers,
            )

    def send_html_email(
        self, to_email: str, subject: str, html_content: str
    ) -> Dict[str, Any]:
        """Send HTML email."""
        email_data = {
            "to": to_email,
            "subject": subject,
            "message": html_content,
            "content_type": "html",
        }

        if self.email_auth_key:
            email_data["authkey"] = self.email_auth_key
        else:
            email_data["username"] = self.email_username
            email_data["password"] = self.email_password

        return self._make_request("POST", self.email_base_url + "/", json=email_data)

    def send_bulk_email(
        self, recipients: List[Dict[str, str]], subject: str, message: str
    ) -> Dict[str, Any]:
        """Send bulk emails."""
        results = []
        for recipient in recipients:
            result = self.send_email(
                to_email=recipient["email"], subject=subject, message=message
            )
            results.append(result)

        # Return overall status
        if all(r.get("status") == "success" for r in results):
            return {"status": "success", "sent_count": len(results)}
        else:
            return {"status": "partial", "results": results}

    def send_email_with_template(
        self, to_email: str, template: Dict[str, str], template_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Send email using template."""
        # Process template
        subject = template["subject"]
        message = template["body"]

        # Replace template variables
        for key, value in template_data.items():
            placeholder = f"{{{{{key}}}}}"
            subject = subject.replace(placeholder, str(value))
            message = message.replace(placeholder, str(value))

        return self.send_email(to_email, subject, message)

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
        """Handle email delivery callback."""
        if "message_id" in callback_data and "status" in callback_data:
            return {
                "processed": True,
                "message_id": callback_data["message_id"],
                "status": callback_data["status"],
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
