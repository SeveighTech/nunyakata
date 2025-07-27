# Nalo Solutions Integration

Nalo Solutions provides comprehensive payment, SMS, email, and USSD services for Ghana and West Africa.

## Overview

The `NaloSolutions` client provides access to:

- **Payment Processing** - Mobile money and bank transfers
- **SMS Messaging** - Bulk SMS and notifications  
- **Email Services** - Transactional and bulk emails
- **USSD Applications** - Interactive USSD sessions

## Quick Setup

```python
from nunyakata import NaloSolutions

client = NaloSolutions(
    # SMS Configuration
    sms_username="your_sms_username",
    sms_password="your_sms_password", 
    sms_source="YOUR_SENDER_ID",
    
    # Payment Configuration
    payment_username="your_payment_username",
    payment_password="your_payment_password",
    merchant_id="your_merchant_id",
    
    # Email Configuration  
    email_username="your_email_username",
    email_password="your_email_password"
)
```

## Authentication Methods

### Method 1: Username/Password
```python
client = NaloSolutions(
    sms_username="username",
    sms_password="password",
    email_username="username", 
    email_password="password"
)
```

### Method 2: Auth Key
```python
client = NaloSolutions(
    sms_auth_key="your_auth_key",
    email_auth_key="your_auth_key"
)
```

### Method 3: Environment Variables
```python
from nunyakata import load_nalo_client_from_env

# Loads configuration from environment variables
client = load_nalo_client_from_env()
```

## Payment Services

### Make Payment
```python
response = client.make_payment(
    amount=50.00,
    customer_number="233501234567",
    customer_name="John Doe",
    item_desc="Product Purchase",
    order_id="ORDER_001",
    payby="MTN",  # MTN, VODAFONE, AIRTELTIGO
    callback_url="https://yoursite.com/callback"
)

print(f"Payment Status: {response['status']}")
print(f"Transaction ID: {response.get('transaction_id')}")
```

### Simple Payment
```python
response = client.make_simple_payment(
    amount=25.00,
    phone_number="233501234567",
    wallet_type="mtn"
)
```

### Handle Payment Callback
```python
# In your webhook endpoint
callback_data = request.json  # From your web framework
result = client.handle_payment_callback(callback_data)

if result['status'] == 'success':
    # Payment successful
    print(f"Payment confirmed: {result['transaction_id']}")
```

## SMS Services

### Send SMS
```python
response = client.send_sms(
    phone_number="233501234567",
    message="Hello from Nunyakata!",
    sender_id="CUSTOM_ID"  # Optional
)

print(f"SMS Status: {response['status']}")
print(f"Message ID: {response.get('message_id')}")
```

### Bulk SMS
```python
recipients = ["233501234567", "233507654321", "233551122334"]
response = client.send_sms(
    phone_number=recipients,
    message="Bulk message to multiple recipients"
)
```

## Email Services

### Send Email
```python
response = client.send_email(
    recipient="user@example.com",
    sender="noreply@yoursite.com", 
    subject="Welcome to Our Service",
    message="Thank you for signing up!",
    sender_name="Your Company"
)
```

### Send HTML Email
```python
html_content = """
<html>
<body>
    <h1>Welcome!</h1>
    <p>Thank you for joining us.</p>
</body>
</html>
"""

response = client.send_email(
    recipient="user@example.com",
    sender="noreply@yoursite.com",
    subject="Welcome!",
    message=html_content,
    is_html=True
)
```

### Bulk Email
```python
recipients = [
    {"email": "user1@example.com", "name": "User One"},
    {"email": "user2@example.com", "name": "User Two"}
]

response = client.send_email(
    recipient=recipients,
    sender="noreply@yoursite.com",
    subject="Newsletter",
    message="Monthly newsletter content"
)
```

## USSD Services

### Handle USSD Request
```python
# In your USSD webhook endpoint
ussd_data = {
    "sessionid": "12345",
    "msisdn": "233501234567", 
    "userdata": "*123#",
    "msgtype": True
}

response = client.handle_ussd_request(ussd_data)

print(f"USSD Response: {response['msg']}")
print(f"Continue Session: {response['msgtype']}")
```

### Create Custom USSD Menu
```python
menu = client.create_ussd_menu(
    title="Main Menu",
    options=[
        "1. Check Balance",
        "2. Transfer Money", 
        "3. Buy Airtime"
    ],
    footer="Enter your choice:"
)

response = client.create_ussd_response(
    message=menu,
    continue_session=True
)
```

## Error Handling

```python
try:
    response = client.send_sms("233501234567", "Test message")
    
    if response.get('status') == 'success':
        print("SMS sent successfully!")
    else:
        print(f"SMS failed: {response.get('message')}")
        
except Exception as e:
    print(f"Error: {e}")
```

## Configuration Options

### Custom API URLs
```python
client = NaloSolutions(
    sms_username="username",
    sms_password="password",
    sms_base_url="https://custom-sms-api.com",
    payment_base_url="https://custom-payment-api.com"
)
```

### Timeout Settings
```python
client = NaloSolutions(
    sms_username="username", 
    sms_password="password",
    timeout=30  # 30 second timeout
)
```

## Best Practices

1. **Store credentials securely** - Use environment variables
2. **Handle errors gracefully** - Always check response status
3. **Validate phone numbers** - Ensure proper format (233XXXXXXXXX)
4. **Test in sandbox** - Use test credentials during development
5. **Monitor usage** - Track API calls and costs
6. **Cache responses** - Store transaction IDs for reference

## Next Steps

- [Payment Examples](../examples/payments.md)
- [SMS Examples](../examples/sms.md)
- [Email Examples](../examples/email.md)
- [USSD Examples](../examples/ussd.md)
