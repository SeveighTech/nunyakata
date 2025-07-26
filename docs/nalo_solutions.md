# Nalo Solutions Integration

This document explains how to use the Nalo Solutions API integration in the nunyakata package.

## Overview

Nalo Solutions provides four main services for Ghana:

1. **Mobile Money Payments** - Process payments via MTN, Vodafone, AirtelTigo
2. **SMS** - Send single and bulk SMS messages
3. **USSD** - Handle interactive USSD sessions
4. **Email** - Send emails (implementation depends on Nalo's email API)

## Installation

```bash
pip install nunyakata
```

## Quick Start

```python
from nunyakata import NaloSolutionsClient

# Initialize client with your credentials
client = NaloSolutionsClient(
    # Payment credentials
    payment_username="your_payment_username",
    payment_password="your_payment_password",
    merchant_id="your_merchant_id",

    # SMS credentials
    sms_username="your_sms_username",
    sms_password="your_sms_password",
    sms_source="your_sender_id"
)

# Send SMS
result = client.send_sms("233123456789", "Hello from Ghana!")
print(result)

# Process mobile money payment
payment = client.make_payment(
    order_id="ORDER123",
    key="KEY123",
    phone_number="233123456789",
    item_desc="Product Purchase",
    amount=25.00,
    network="MTN"
)
print(payment)
```

## Services Documentation

### 1. Mobile Money Payments

Process payments via Ghana's mobile money networks:

```python
# Make a payment
result = client.make_payment(
    order_id="unique_order_id",
    key="transaction_key",
    phone_number="233123456789",
    item_desc="Product description",
    amount=10.00,
    network="MTN",  # Options: MTN, VODAFONE, AIRTELTIGO
    customer_name="Customer Name",
    callback_url="https://yoursite.com/callback",  # Optional
    is_ussd=True  # Whether to use USSD flow
)
```

**Networks supported:**

- `MTN` - MTN Mobile Money
- `VODAFONE` - Vodafone Cash
- `AIRTELTIGO` - AirtelTigo Money

### 2. SMS Services

Send SMS messages to Ghana phone numbers:

```python
# Send single SMS
result = client.send_sms(
    recipient="233123456789",
    message="Your message here",
    delivery_report=True
)

# Send bulk SMS
recipients = ["233123456789", "233987654321", "233555666777"]
results = client.send_bulk_sms(
    recipients=recipients,
    message="Bulk message for everyone"
)
```

### 3. USSD Services

Handle interactive USSD sessions:

```python
# Handle USSD request (typically in a webhook)
ussd_data = {
    "USERID": "user_123",
    "MSISDN": "233123456789",
    "USERDATA": "1",  # User input
    "MSGTYPE": False,  # False=continuing, True=new session
    "SESSIONID": "session_123",
    "NETWORK": "MTN"
}

response = client.handle_ussd_request(ussd_data)
# Returns formatted response for Nalo USSD gateway
```

**USSD Response Format:**

```python
{
    "USERID": "user_123",
    "MSISDN": "233123456789",
    "MSG": "Your response message to user",
    "MSGTYPE": True,  # True=continue session, False=end session
    "SESSIONID": "session_123",
    "NETWORK": "MTN"
}
```

### 4. Email Services

Send emails via Nalo Solutions:

```python
result = client.send_email(
    to_email="recipient@example.com",
    subject="Email Subject",
    message="Email content here",
    from_email="sender@yoursite.com"  # Optional
)
```

## Environment Variables

For security, use environment variables for credentials:

```bash
# Payment API
export NALO_PAYMENT_USERNAME="your_payment_username"
export NALO_PAYMENT_PASSWORD="your_payment_password"
export NALO_MERCHANT_ID="your_merchant_id"

# SMS API
export NALO_SMS_USERNAME="your_sms_username"
export NALO_SMS_PASSWORD="your_sms_password"
export NALO_SMS_SOURCE="your_sender_id"
```

Then use them in your code:

```python
import os
from nunyakata import NaloSolutionsClient

client = NaloSolutionsClient(
    payment_username=os.getenv("NALO_PAYMENT_USERNAME"),
    payment_password=os.getenv("NALO_PAYMENT_PASSWORD"),
    merchant_id=os.getenv("NALO_MERCHANT_ID"),
    sms_username=os.getenv("NALO_SMS_USERNAME"),
    sms_password=os.getenv("NALO_SMS_PASSWORD"),
    sms_source=os.getenv("NALO_SMS_SOURCE")
)
```

## Flask Integration Example

For USSD webhooks with Flask:

```python
from flask import Flask, request, jsonify
from nunyakata import NaloSolutionsClient
import os

app = Flask(__name__)
client = NaloSolutionsClient(
    sms_username=os.getenv("NALO_SMS_USERNAME"),
    sms_password=os.getenv("NALO_SMS_PASSWORD"),
    sms_source=os.getenv("NALO_SMS_SOURCE")
)

@app.route("/ussd-webhook", methods=["POST"])
def handle_ussd():
    ussd_data = request.get_json()
    response = client.handle_ussd_request(ussd_data)
    return jsonify(response)

if __name__ == "__main__":
    app.run(port=5000)
```

## Error Handling

The client raises exceptions for various error conditions:

```python
try:
    result = client.send_sms("233123456789", "Test message")
except ValueError as e:
    print(f"Configuration error: {e}")
except requests.exceptions.RequestException as e:
    print(f"Network error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Testing

The package includes comprehensive tests. Run them with:

```bash
pytest tests/test_nalo_solutions.py -v
```

## API Reference

### NaloSolutionsClient

**Constructor Parameters:**

- `payment_username` (str, optional): Username for payment API
- `payment_password` (str, optional): Password for payment API
- `merchant_id` (str, optional): Merchant ID for payments
- `sms_username` (str, optional): Username for SMS API
- `sms_password` (str, optional): Password for SMS API
- `sms_source` (str, optional): SMS sender ID
- `payment_base_url` (str): Base URL for payment API
- `sms_base_url` (str): Base URL for SMS API
- `api_key` (str, optional): General API key

**Methods:**

- `make_payment()` - Process mobile money payment
- `send_sms()` - Send single SMS
- `send_bulk_sms()` - Send SMS to multiple recipients
- `handle_ussd_request()` - Handle USSD session
- `send_email()` - Send email
- `get_service_status()` - Check service availability
- `check_balance()` - Check account balance

## Support

For issues with the nunyakata package, please open an issue on GitHub.
For Nalo Solutions API support, contact Nalo Solutions directly.
