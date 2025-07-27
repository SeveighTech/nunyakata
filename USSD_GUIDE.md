# USSD Implementation Guide

## Overview

The USSD implementation in the `nunyakata` package provides a clean, generic framework for building USSD applications that work with Nalo Solutions' USSD API. The implementation focuses purely on USSD session management and menu handling, without any payment-specific logic.

## Key Features

- **Nalo API Compliance**: Follows the exact format required by Nalo Solutions USSD API
- **Session Management**: Automatic session creation, tracking, and cleanup
- **Generic Implementation**: No payment processing - easily extensible for any business logic
- **Input Validation**: Built-in validation for phone numbers, amounts, and user inputs
- **Menu Helpers**: Utility methods for creating USSD menus and responses

## Basic Usage

### 1. Initialize the Client

```python
from nunyakata import NaloSolutions

# Basic initialization
client = NaloSolutions(
    ussd_userid="YOUR_USERID",  # Provided by Nalo Solutions
    ussd_environment="sandbox"  # or "production"
)
```

### 2. Handle USSD Requests

The main method for handling USSD requests follows the Nalo API format:

```python
# Example request from Nalo API
request_data = {
    "USERID": "NALOTest",
    "MSISDN": "233265542141",           # User's phone number
    "USERDATA": "1",                    # User input
    "MSGTYPE": False,                   # True for initial, False for subsequent
    "NETWORK": "MTN",                   # User's network
    "SESSIONID": "unique_session_id"    # Session identifier
}

# Handle the request
response = client.handle_ussd_request(request_data)

# Response format (to be sent back to Nalo API)
{
    "USERID": "NALOTest",
    "MSISDN": "233265542141",
    "USERDATA": "1",
    "MSG": "Your response message here",
    "MSGTYPE": True  # True to continue session, False to end
}
```

## Session Flow

### 1. Initial Request (MSGTYPE = True)

- User dials the USSD code
- Nalo sends initial request with `MSGTYPE: True`
- Your app returns welcome menu

### 2. Subsequent Requests (MSGTYPE = False)

- User makes selections
- Session tracks the current stage and user data
- Your app processes input and returns appropriate responses

### 3. Session Management

Sessions are automatically managed with these stages:

- **Stage 0**: Main menu
- **Stage 1**: Sub-menus and service selection
- **Stage 2**: Final processing

## Extending for Custom Business Logic

The default implementation provides a generic demo. To add your business logic, extend the class and override specific methods:

```python
class MyCustomUSSD(NaloSolutions):
    def _handle_service_menu(self, userid, msisdn, userdata, network, sessionid, service):
        """Override this method to implement your business logic."""

        if service == "services":
            try:
                selection = int(userdata.strip())

                if selection == 1:
                    # Your Service A logic here
                    # Could integrate with payment API, send SMS, etc.
                    msg = f"Service A activated for {msisdn}"

                elif selection == 2:
                    # Your Service B logic here
                    msg = "Service B - Processing your request..."

                elif selection == 3:
                    # Your Service C logic here
                    msg = "Service C completed successfully"

                else:
                    msg = "Invalid selection. Please choose 1-3."

                return self._create_nalo_ussd_response(
                    userid, msisdn, userdata, msg, False
                )

            except ValueError:
                msg = "Please enter a valid number."
                return self._create_nalo_ussd_response(
                    userid, msisdn, userdata, msg, False
                )

        # Call parent implementation for other services
        return super()._handle_service_menu(userid, msisdn, userdata, network, sessionid, service)

# Use your custom implementation
custom_client = MyCustomUSSD(ussd_userid="YOUR_USERID")
```

## Integration Examples

### 1. Flask Web Application

```python
from flask import Flask, request, jsonify
from nunyakata import NaloSolutions

app = Flask(__name__)
ussd_client = NaloSolutions(ussd_userid="YOUR_USERID")

@app.route("/ussd-endpoint", methods=["POST"])
def handle_ussd():
    # Get request data from Nalo API
    request_data = request.get_json()

    # Process the USSD request
    response = ussd_client.handle_ussd_request(request_data)

    # Return response to Nalo API
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
```

### 2. Integrating with Payment Services

```python
class PaymentUSSD(NaloSolutions):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Initialize payment client separately
        self.payment_client = NaloSolutions(
            payment_merchant_id="YOUR_MERCHANT_ID",
            payment_username="YOUR_USERNAME",
            payment_password="YOUR_PASSWORD"
        )

    def _handle_service_menu(self, userid, msisdn, userdata, network, sessionid, service):
        if service == "payment":
            # Handle payment logic
            amount = 10.0  # Get from user input or session

            # Use the payment API
            payment_response = self.payment_client.make_simple_payment(
                amount=amount,
                phone_number=msisdn,
                customer_name="USSD User",
                description="USSD Payment",
                callback_url="https://your-app.com/payment-callback"
            )

            if payment_response.get("status") == "success":
                msg = "Payment initiated successfully!"
            else:
                msg = "Payment failed. Please try again."

            return self._create_nalo_ussd_response(
                userid, msisdn, userdata, msg, False
            )

        return super()._handle_service_menu(userid, msisdn, userdata, network, sessionid, service)
```

### 3. Integrating with SMS Services

```python
class SMSUSSD(NaloSolutions):
    def _handle_service_menu(self, userid, msisdn, userdata, network, sessionid, service):
        if service == "sms":
            # Get recipient from session data
            session = self.get_ussd_session(sessionid)
            recipient = session.get("data", {}).get("sms_recipient")

            if recipient:
                # Send SMS
                sms_response = self.send_sms(
                    phone_number=recipient,
                    message=userdata,  # User's message input
                    sender_id="YOUR_SENDER_ID"
                )

                if sms_response.get("status") == "success":
                    msg = f"SMS sent to {recipient} successfully!"
                else:
                    msg = "SMS sending failed. Please try again."

                return self._create_nalo_ussd_response(
                    userid, msisdn, userdata, msg, False
                )

        return super()._handle_service_menu(userid, msisdn, userdata, network, sessionid, service)
```

## Utility Methods

### Validation

```python
# Phone number validation
is_valid = client.validate_phone_number("0265542141")

# Amount validation
is_valid = client.validate_amount("10.50")

# Custom input validation
is_valid = client.validate_ussd_input("1", ["1", "2", "3"])
```

### Menu Creation

```python
# Create USSD menu
menu = client.create_ussd_menu(
    title="Main Menu",
    options=["Check Balance", "Send Money", "Buy Airtime"],
    footer="0. Exit"
)
```

### Session Management

```python
# Get session data
session = client.get_ussd_session(sessionid)

# Update session data
client.update_ussd_session(sessionid, {
    "stage": 2,
    "user_selection": "option_1",
    "amount": 50.0
})

# Clear session
client.clear_ussd_session(sessionid)
```

## API Reference

### Main Methods

- `handle_ussd_request(request_data)`: Main handler for USSD requests
- `_handle_service_menu(...)`: Override this for custom business logic

### Session Methods

- `get_ussd_session(sessionid)`: Get session data
- `update_ussd_session(sessionid, data)`: Update session data
- `clear_ussd_session(sessionid)`: Clear session data

### Validation Methods

- `validate_phone_number(phone)`: Validate Ghana phone numbers
- `validate_amount(amount)`: Validate monetary amounts
- `validate_ussd_input(input, options)`: Validate user input against options

### Utility Methods

- `create_ussd_menu(title, options, footer)`: Create formatted menus
- `create_ussd_response(message, continue_session)`: Create response objects
- `_create_nalo_ussd_response(...)`: Create Nalo API format responses

## Best Practices

1. **Always validate user input** before processing
2. **Keep messages concise** (160 characters or less for best compatibility)
3. **Handle errors gracefully** with user-friendly messages
4. **Clear sessions** when transactions complete
5. **Use the session data** to maintain state across requests
6. **Override `_handle_service_menu()`** for custom business logic
7. **Keep USSD logic separate** from payment/SMS processing

## Testing

The package includes comprehensive tests. Run them with:

```bash
python3 test_ussd.py
```

This will test:

- Basic USSD session flow
- Menu navigation
- Session management
- Input validation
- Custom implementation examples

## Production Deployment

1. Set up your endpoint URL with Nalo Solutions
2. Configure your web server to handle POST requests
3. Use HTTPS for security
4. Implement proper logging and monitoring
5. Test thoroughly in sandbox before going live

For production use, you'll need:

- Valid USERID from Nalo Solutions
- Registered USSD shortcode
- SSL certificate for your endpoint
- Proper error handling and logging
