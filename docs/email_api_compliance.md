# Nalo Solutions Email API - 100% Compliance Documentation

This document details the complete implementation of Nalo Solutions Email API, ensuring 100% compliance with the official API documentation.

## Overview

The Email API implementation supports all features documented in the official Nalo Solutions Email API specification:

- **JSON-based email sending** with username/password or auth key authentication
- **Form-data email sending** with file attachments
- **Bulk email support** for multiple recipients
- **Template support** with content placeholders
- **HTML email** capabilities
- **Callback handling** for delivery status
- **Comprehensive error handling** with proper status codes

## Authentication Methods

### Method 1: Username and Password

```python
client = NaloSolutionsClient(
    email_username="your_username",
    email_password="your_password"
)
```

### Method 2: Auth Key

```python
client = NaloSolutionsClient(
    email_auth_key="your_long_auth_key"
)
```

## API Endpoint

**Base URL:** `https://sms.nalosolutions.com/clientapi/Nal_resl/send-email/`

All email operations use POST requests to this endpoint.

## Core Implementation Features

### 1. Basic Email Sending (JSON)

**Method:** `send_email()`

**Request Format:**

```json
{
  "username": "nalo_fiifi",
  "password": "qwerty@123",
  "emailTo": ["alexanderadadd@gmail.com", "makoto@nalosolutions.com"],
  "emailFrom": "aadade@nalosolutions.com",
  "emailBody": "Your email content here...",
  "senderName": "Alex",
  "subject": "Pushing the limit with Mina And Pk",
  "callBackUrl": "http://127.0.0.1:8001/api"
}
```

**Response Format:**

```json
{
  "email_job_id": "api.1.20220623.6FxcpucGNVXZhLeMj6euFS",
  "total_valid_emails": 1,
  "total_invalid_emails": 0,
  "total_cost": 0.002,
  "status": true,
  "invalid_emails": [],
  "total_duplicates": 0
}
```

### 2. Email with File Attachments (Form-Data)

**Method:** `send_email()` with `attachment_path` parameter

**Request Format:** Multipart form-data with file upload

- Uses form fields for email parameters
- File attached as `attach_file` field
- Supports multiple recipients with indexed format: `emailTo[0]`, `emailTo[1]`

### 3. Auth Key Authentication

**Method:** All email methods support auth key

**Request Format:**

```json
{
  "key": "@z0!!whci#!llf4yzcydd7uoaq5i4q(lnmknknjnlmkpcFJFVVEF..ACFWFSDSAC,CWDW",
  "emailTo": ["alexandera@gmail.com"],
  "emailFrom": "example@example.com",
  "emailBody": "Email content...",
  "senderName": "Alex",
  "subject": "Subject",
  "callBackUrl": ""
}
```

### 4. Template Support

**Method:** `send_email_with_template()`

Templates use `{{{content}}}` placeholder for dynamic content insertion.

### 5. HTML Email Support

**Method:** `send_html_email()`

Supports encoded HTML content for rich email formatting.

## Required Headers

All requests include the User-Agent header as specified:

```
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36
```

## Status Codes

| Code | Description                                                                                 |
| ---- | ------------------------------------------------------------------------------------------- |
| 200  | Accepted; Single email dispatch is accepted and processed to the recipient                  |
| 400  | Validation failed; if any required parameter is missing in the request object               |
| 401  | Unauthorized; if username, password or key is wrong                                         |
| 412  | Precondition failed; if the api call failed to meet business and application specific rules |
| 500  | Server and Application level error                                                          |

## Callback Handling

**Callback Parameters:**

- `mid`: unique id for the email
- `sender_address`: sender email address
- `destination_address`: recipient address
- `timestamp`: date and time mail was sent
- `status_desc`: the state of that particular email job

**Implementation:** `handle_email_callback()` method processes callback data and returns acknowledgment.

## Email Verification Requirement

⚠️ **Important**: All sender emails must be verified through the Nalo Solutions email portal before use:

1. Login to Nalo portal
2. Navigate to Email tab → Sender Email
3. Enter your sender email address
4. Check verification email and click verification link
5. Email will be added to verified sender list

## Implementation Methods

### Core Methods

- `send_email()` - Universal email sending method
- `send_bulk_email()` - Send to multiple recipients
- `send_html_email()` - Send HTML formatted emails
- `send_email_with_template()` - Use predefined templates
- `handle_email_callback()` - Process delivery callbacks

### Utility Methods

- `parse_email_response()` - Parse API responses
- `get_email_status_codes()` - Get status code descriptions
- `_send_email_json()` - Internal JSON method
- `_send_email_with_attachment()` - Internal form-data method

## Configuration

### Environment Variables

```bash
# Method 1: Username/Password
NALO_EMAIL_USERNAME=your_username
NALO_EMAIL_PASSWORD=your_password

# Method 2: Auth Key (alternative)
NALO_EMAIL_AUTH_KEY=your_auth_key

# Optional: Custom endpoint
NALO_EMAIL_BASE_URL=https://sms.nalosolutions.com/clientapi/Nal_resl/send-email/
```

### Client Initialization

```python
from nunyakata import load_nalo_client_from_env

# Load from environment
client = load_nalo_client_from_env()

# Manual configuration
client = NaloSolutionsClient(
    email_username="your_username",
    email_password="your_password",
    # OR
    email_auth_key="your_auth_key"
)
```

## Example Usage

### Basic Email

```python
response = client.send_email(
    email_to="recipient@example.com",
    email_from="verified@yourdomain.com",  # Must be verified!
    subject="Test Email",
    email_body="Hello from Nalo Solutions!",
    sender_name="Your Name",
    callback_url="https://yoursite.com/webhooks/email"
)
```

### Bulk Email

```python
response = client.send_bulk_email(
    recipients=["user1@example.com", "user2@example.com"],
    email_from="verified@yourdomain.com",
    subject="Bulk Notification",
    email_body="Important update for all users",
    sender_name="Admin"
)
```

### HTML Email

```python
html_content = """
<html>
<body>
    <h1>Welcome!</h1>
    <p>This is an <strong>HTML email</strong>.</p>
</body>
</html>
"""

response = client.send_html_email(
    email_to="recipient@example.com",
    email_from="verified@yourdomain.com",
    subject="HTML Newsletter",
    html_content=html_content,
    sender_name="Newsletter Team"
)
```

### Email with Attachment

```python
response = client.send_email(
    email_to="recipient@example.com",
    email_from="verified@yourdomain.com",
    subject="Document Attached",
    email_body="Please find the attached document.",
    sender_name="Document Sender",
    attachment_path="/path/to/file.pdf"
)
```

## Compliance Checklist

✅ **Authentication Methods**

- [x] Username/password authentication
- [x] Auth key authentication

✅ **Request Formats**

- [x] JSON payload for basic emails
- [x] Form-data for file attachments
- [x] Multiple recipient support
- [x] Required User-Agent header

✅ **Response Handling**

- [x] Proper response parsing
- [x] Status code interpretation
- [x] Error handling

✅ **Advanced Features**

- [x] Template support with {{{content}}} placeholder
- [x] HTML email support
- [x] File attachment support
- [x] Bulk email capabilities

✅ **Callback Support**

- [x] Callback data processing
- [x] Proper acknowledgment response

✅ **Configuration**

- [x] Environment variable support
- [x] Flexible client initialization
- [x] Service status checking

## Testing

Run comprehensive email tests:

```bash
python examples/email_comprehensive_demo.py
```

Start webhook server for callback testing:

```bash
python examples/email_comprehensive_demo.py --webhook --port 5000
```

## Production Considerations

1. **Email Verification**: Ensure all sender emails are verified in Nalo portal
2. **Callback Endpoints**: Set up proper webhook endpoints for delivery status
3. **Error Handling**: Implement proper error handling for all status codes
4. **Rate Limiting**: Monitor usage to avoid exceeding API limits
5. **Cost Monitoring**: Track email costs and balance
6. **Template Management**: Use templates for consistent branding

## Official API Documentation Compliance

This implementation is 100% compliant with the official Nalo Solutions Email API documentation, including:

- Exact request/response formats
- Proper authentication methods
- Required headers and parameters
- File attachment handling
- Template and HTML support
- Callback processing
- Status code handling

All examples and methods match the official API specification exactly.
