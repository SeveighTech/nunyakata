#!/usr/bin/env python3
"""
Test script for Email functionality with the correct Nalo API implementation.
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from nunyakata import NaloSolutions


def test_email_api():
    """Test Email API functionality."""
    print("🧪 Testing Email API...")

    # Initialize the client with email credentials
    # Note: These are demo credentials - replace with real ones for actual testing
    client = NaloSolutions(
        email_username="demo_user",
        email_password="demo_password",
        email_from_email="sender@example.com",
        email_from_name="Demo Sender",
    )

    print(f"📧 Email API URL: {client.email_base_url}")

    # Test 1: Single email
    print("\n1️⃣ Testing single email...")
    try:
        response = client.send_email(
            to_email="recipient@example.com",
            subject="Test Email from Nunyakata",
            message="This is a test email sent using the Nalo Solutions Email API.",
            sender_name="Test Sender",
        )
        print("Single Email Response:")
        print(f"  Status: {response.get('status', 'Unknown')}")
        if response.get("status") == "success":
            print("  ✅ Email API structure is correct")
        else:
            print(f"  Response: {response}")
    except Exception as e:
        print(f"  ❌ Error: {e}")

    # Test 2: Multiple recipients
    print("\n2️⃣ Testing bulk email (multiple recipients)...")
    try:
        response = client.send_bulk_email(
            recipients=["user1@example.com", "user2@example.com", "user3@example.com"],
            subject="Bulk Email Test",
            message="This is a bulk email test message.",
            sender_name="Bulk Sender",
        )
        print("Bulk Email Response:")
        print(f"  Status: {response.get('status', 'Unknown')}")
        if response.get("status") == "success":
            print("  ✅ Bulk email API structure is correct")
        else:
            print(f"  Response: {response}")
    except Exception as e:
        print(f"  ❌ Error: {e}")

    # Test 3: HTML email
    print("\n3️⃣ Testing HTML email...")
    try:
        html_content = """
        <html>
        <body>
            <h1>Test HTML Email</h1>
            <p>This is a <strong>test HTML email</strong> with formatting.</p>
            <ul>
                <li>Feature 1</li>
                <li>Feature 2</li>
                <li>Feature 3</li>
            </ul>
        </body>
        </html>
        """
        response = client.send_html_email(
            to_email="htmltest@example.com",
            subject="HTML Email Test",
            html_content=html_content,
            sender_name="HTML Sender",
        )
        print("HTML Email Response:")
        print(f"  Status: {response.get('status', 'Unknown')}")
        if response.get("status") == "success":
            print("  ✅ HTML email API structure is correct")
        else:
            print(f"  Response: {response}")
    except Exception as e:
        print(f"  ❌ Error: {e}")

    # Test 4: Template email
    print("\n4️⃣ Testing template email...")
    try:
        response = client.send_email_with_template(
            to_email="template@example.com",
            template_name="welcome_template",
            content="Welcome to our service! We're excited to have you on board.",
            subject="Welcome to Our Service",
            sender_name="Welcome Team",
        )
        print("Template Email Response:")
        print(f"  Status: {response.get('status', 'Unknown')}")
        if response.get("status") == "success":
            print("  ✅ Template email API structure is correct")
        else:
            print(f"  Response: {response}")
    except Exception as e:
        print(f"  ❌ Error: {e}")

    # Test 5: Email with callback URL
    print("\n5️⃣ Testing email with callback URL...")
    try:
        response = client.send_email(
            to_email="callback@example.com",
            subject="Email with Callback",
            message="This email includes a callback URL for delivery tracking.",
            callback_url="https://your-app.com/email-callback",
            sender_name="Callback Sender",
        )
        print("Callback Email Response:")
        print(f"  Status: {response.get('status', 'Unknown')}")
        if response.get("status") == "success":
            print("  ✅ Callback email API structure is correct")
        else:
            print(f"  Response: {response}")
    except Exception as e:
        print(f"  ❌ Error: {e}")

    print("\n✅ Email API testing completed!")


def test_email_validation():
    """Test email validation functionality."""
    print("\n🧪 Testing Email Validation...")

    client = NaloSolutions()

    test_emails = [
        ("valid@example.com", True),
        ("user.name@domain.co.uk", True),
        ("test123@gmail.com", True),
        ("invalid.email", False),
        ("@domain.com", False),
        ("user@", False),
        ("", False),
        ("user name@domain.com", False),  # Space in email
        ("user@domain", False),  # No TLD
    ]

    print("\n📧 Testing email validation...")
    for email, expected in test_emails:
        is_valid = client.validate_email(email)
        status = "✅" if is_valid == expected else "❌"
        print(f"  {email:25} -> {status} {'Valid' if is_valid else 'Invalid'}")


def test_email_callback_handling():
    """Test email callback handling."""
    print("\n🧪 Testing Email Callback Handling...")

    client = NaloSolutions()

    # Test valid callback
    print("\n📨 Testing valid callback...")
    valid_callback = {
        "mid": "api.1.20220623.6FxcpucGNVXZhLeMj6euFS",
        "sender_address": "sender@example.com",
        "destination_address": "recipient@example.com",
        "timestamp": "2022-06-23T10:30:00Z",
        "status_desc": "delivered",
    }

    result = client.handle_email_callback(valid_callback)
    print(f"  Processed: {result['processed']}")
    print(f"  Email ID: {result.get('email_id')}")
    print(f"  Status: {result.get('status')}")

    # Test invalid callback
    print("\n📨 Testing invalid callback...")
    invalid_callback = {"invalid_field": "test"}

    result = client.handle_email_callback(invalid_callback)
    print(f"  Processed: {result['processed']}")
    print(f"  Error: {result.get('error')}")


def demonstrate_email_api_usage():
    """Demonstrate how to use the Email API in real applications."""
    print("\n🧪 Email API Usage Examples...")

    print("\n📋 Basic Usage Example:")
    print(
        """
# Initialize client
client = NaloSolutions(
    email_username="your_username",
    email_password="your_password",
    email_from_email="verified@yourdomain.com",  # Must be verified!
    email_from_name="Your App Name"
)

# Send simple email
response = client.send_email(
    to_email="user@example.com",
    subject="Welcome!",
    message="Welcome to our service!"
)

# Send to multiple recipients
response = client.send_bulk_email(
    recipients=["user1@example.com", "user2@example.com"],
    subject="Newsletter",
    message="Check out our latest updates!"
)

# Send HTML email
response = client.send_html_email(
    to_email="user@example.com",
    subject="Rich Content",
    html_content="<h1>Hello!</h1><p>Rich <strong>HTML</strong> content</p>"
)

# Send with template
response = client.send_email_with_template(
    to_email="user@example.com",
    template_name="welcome_template",
    content="Welcome to our platform!",
    subject="Welcome!"
)
    """
    )

    print("\n📋 Integration with Flask Example:")
    print(
        """
from flask import Flask, request, jsonify
from nunyakata import NaloSolutions

app = Flask(__name__)
email_client = NaloSolutions(
    email_username="your_username",
    email_password="your_password",
    email_from_email="noreply@yourapp.com"
)

@app.route("/send-welcome-email", methods=["POST"])
def send_welcome():
    data = request.get_json()
    
    response = email_client.send_email(
        to_email=data["email"],
        subject="Welcome to Our Service!",
        message=f"Hello {data['name']}, welcome to our platform!",
        sender_name="Welcome Team"
    )
    
    if response.get("status") == "success":
        return jsonify({"success": True, "email_job_id": response.get("email_job_id")})
    else:
        return jsonify({"success": False, "error": response.get("message")})

@app.route("/email-callback", methods=["POST"])
def email_callback():
    callback_data = request.get_json()
    result = email_client.handle_email_callback(callback_data)
    
    if result["processed"]:
        # Update your database with delivery status
        # log_email_delivery(result["email_id"], result["status"])
        pass
    
    return jsonify({"received": True})
    """
    )


if __name__ == "__main__":
    print("🚀 Email API Test Suite")
    print("=" * 50)

    try:
        test_email_api()
        test_email_validation()
        test_email_callback_handling()
        demonstrate_email_api_usage()

        print("\n🎉 All email tests completed!")
        print("\n📝 Implementation Notes:")
        print("• Email API uses correct Nalo endpoint: /clientapi/Nal_resl/send-email/")
        print("• Supports single and bulk emails")
        print("• Handles HTML content and templates")
        print("• Supports file attachments")
        print("• Includes callback handling for delivery status")
        print("• All sender emails must be verified through Nalo portal")
        print("• Uses proper parameter names: emailTo, emailFrom, emailBody, etc.")

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback

        traceback.print_exc()
