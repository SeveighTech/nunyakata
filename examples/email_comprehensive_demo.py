#!/usr/bin/env python3
"""
Comprehensive Email Demo for Nalo Solutions Email API

This example demonstrates all email capabilities including:
- Basic email sending with JSON
- Bulk email sending
- HTML email sending
- Template-based emails
- Email with file attachments
- Callback handling

Run this example:
    python examples/email_comprehensive_demo.py

Make sure to set your credentials in .env file:
    NALO_EMAIL_USERNAME=your_username
    NALO_EMAIL_PASSWORD=your_password
    # OR use auth key instead:
    NALO_EMAIL_AUTH_KEY=your_auth_key
"""

import os
import sys

# Add the src directory to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    print("python-dotenv not installed. Install with: pip install python-dotenv")

try:
    from flask import Flask, request, jsonify

    FLASK_AVAILABLE = True
except ImportError:
    print("Flask not installed. Webhook server will not be available.")
    FLASK_AVAILABLE = False

from nunyakata import load_nalo_client_from_env


class EmailDemoApp:
    """Comprehensive Email API demonstration."""

    def __init__(self):
        """Initialize email demo with Nalo client."""
        try:
            self.client = load_nalo_client_from_env()
            print("✅ Nalo Solutions client initialized successfully")

            # Check service status
            status = self.client.get_service_status()
            print(f"📊 Service Status: {status}")

            if not status["services"]["email"]:
                print(
                    "⚠️  Email service not configured. Please check your email credentials."
                )
                print(
                    "Required: NALO_EMAIL_USERNAME + NALO_EMAIL_PASSWORD OR NALO_EMAIL_AUTH_KEY"
                )

        except Exception as e:
            print(f"❌ Failed to initialize client: {e}")
            sys.exit(1)

    def demo_basic_email(self):
        """Demonstrate basic email sending with JSON payload."""
        print("\n" + "=" * 60)
        print("📧 DEMO: Basic Email Sending")
        print("=" * 60)

        try:
            # NOTE: email_from must be verified in your Nalo email portal
            response = self.client.send_email(
                email_to="recipient@example.com",
                email_from="verified@yourdomain.com",  # Must be verified!
                subject="Test Email from Nalo Solutions",
                email_body="Hello! This is a test email sent via Nalo Solutions Email API. "
                "This demonstrates basic email functionality.",
                sender_name="Demo Sender",
                callback_url="https://yoursite.com/webhooks/email-callback",
            )

            print("✅ Email sent successfully!")
            print(f"📧 Job ID: {response.get('email_job_id')}")
            print(f"📊 Valid Emails: {response.get('total_valid_emails')}")
            print(f"💰 Cost: GHS {response.get('total_cost')}")
            print(f"📋 Full Response: {response}")

            # Parse response for better insights
            parsed = self.client.parse_email_response(response)
            print(f"📈 Success Rate: {parsed['success_rate']:.1f}%")

        except Exception as e:
            print(f"❌ Error sending email: {e}")

    def demo_bulk_email(self):
        """Demonstrate bulk email sending to multiple recipients."""
        print("\n" + "=" * 60)
        print("📧 DEMO: Bulk Email Sending")
        print("=" * 60)

        try:
            recipients = ["user1@example.com", "user2@example.com", "user3@example.com"]

            response = self.client.send_bulk_email(
                recipients=recipients,
                email_from="verified@yourdomain.com",  # Must be verified!
                subject="Bulk Email Notification",
                email_body="This is a bulk email sent to multiple recipients. "
                "Each recipient will receive this same message.",
                sender_name="Bulk Sender",
                callback_url="https://yoursite.com/webhooks/bulk-email-callback",
            )

            print("✅ Bulk email sent successfully!")
            print(f"📧 Job ID: {response.get('email_job_id')}")
            print(f"📊 Total Recipients: {len(recipients)}")
            print(f"✅ Valid Emails: {response.get('total_valid_emails')}")
            print(f"❌ Invalid Emails: {response.get('total_invalid_emails')}")
            print(f"💰 Total Cost: GHS {response.get('total_cost')}")

            if response.get("invalid_emails"):
                print(f"⚠️  Invalid emails: {response['invalid_emails']}")

        except Exception as e:
            print(f"❌ Error sending bulk email: {e}")

    def demo_html_email(self):
        """Demonstrate HTML email sending."""
        print("\n" + "=" * 60)
        print("🎨 DEMO: HTML Email Sending")
        print("=" * 60)

        try:
            html_content = """
            <html>
            <head>
                <style>
                    body { font-family: Arial, sans-serif; }
                    .header { background-color: #4CAF50; color: white; padding: 20px; text-align: center; }
                    .content { padding: 20px; }
                    .footer { background-color: #f1f1f1; padding: 10px; text-align: center; }
                    .button { background-color: #008CBA; color: white; padding: 10px 20px; text-decoration: none; }
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>Welcome to Our Service!</h1>
                </div>
                <div class="content">
                    <p>Hello there!</p>
                    <p>This is a beautifully formatted HTML email sent via Nalo Solutions.</p>
                    <p>
                        <a href="https://example.com/action" class="button">Take Action</a>
                    </p>
                    <p>Best regards,<br>The Team</p>
                </div>
                <div class="footer">
                    <p>© 2025 Your Company. All rights reserved.</p>
                </div>
            </body>
            </html>
            """

            response = self.client.send_html_email(
                email_to="recipient@example.com",
                email_from="verified@yourdomain.com",  # Must be verified!
                subject="Beautiful HTML Email",
                html_content=html_content,
                sender_name="HTML Sender",
                callback_url="https://yoursite.com/webhooks/html-email-callback",
            )

            print("✅ HTML email sent successfully!")
            print(f"📧 Job ID: {response.get('email_job_id')}")
            print(f"🎨 HTML content length: {len(html_content)} characters")
            print(f"💰 Cost: GHS {response.get('total_cost')}")

        except Exception as e:
            print(f"❌ Error sending HTML email: {e}")

    def demo_template_email(self):
        """Demonstrate template-based email sending."""
        print("\n" + "=" * 60)
        print("📝 DEMO: Template-Based Email")
        print("=" * 60)

        try:
            # Assuming you have a template set up in Nalo's cloud platform
            # The template should contain {{{content}}} placeholder
            response = self.client.send_email_with_template(
                email_to="recipient@example.com",
                email_from="verified@yourdomain.com",  # Must be verified!
                subject="Template Email Test",
                sender_name="Template Sender",
                template="welcome_template",  # Your template name/ID
                template_content="Welcome to our platform! Your account has been successfully created. "
                "Please click the verification link to activate your account.",
                callback_url="https://yoursite.com/webhooks/template-email-callback",
            )

            print("✅ Template email sent successfully!")
            print(f"📧 Job ID: {response.get('email_job_id')}")
            print("📝 Template: welcome_template")
            print(f"💰 Cost: GHS {response.get('total_cost')}")

        except Exception as e:
            print(f"❌ Error sending template email: {e}")

    def demo_email_with_attachment(self):
        """Demonstrate email with file attachment."""
        print("\n" + "=" * 60)
        print("📎 DEMO: Email with File Attachment")
        print("=" * 60)

        try:
            # Create a sample file for attachment
            sample_file = "/tmp/sample_attachment.txt"
            with open(sample_file, "w") as f:
                f.write("This is a sample attachment file.\n")
                f.write("Sent via Nalo Solutions Email API.\n")
                f.write("Date: 2025-01-27\n")

            response = self.client.send_email(
                email_to="recipient@example.com",
                email_from="verified@yourdomain.com",  # Must be verified!
                subject="Email with Attachment",
                email_body="Please find the attached file. This email demonstrates "
                "file attachment capabilities of Nalo Solutions Email API.",
                sender_name="Attachment Sender",
                attachment_path=sample_file,
                callback_url="https://yoursite.com/webhooks/attachment-email-callback",
            )

            print("✅ Email with attachment sent successfully!")
            print(f"📧 Job ID: {response.get('email_job_id')}")
            print(f"📎 Attachment: {sample_file}")
            print(f"💰 Cost: GHS {response.get('total_cost')}")

            # Clean up
            os.remove(sample_file)
            print("🧹 Temporary file cleaned up")

        except Exception as e:
            print(f"❌ Error sending email with attachment: {e}")

    def demo_email_status_codes(self):
        """Demonstrate email status codes and error handling."""
        print("\n" + "=" * 60)
        print("📊 DEMO: Email Status Codes")
        print("=" * 60)

        status_codes = self.client.get_email_status_codes()
        print("Email API Status Codes:")
        for code, description in status_codes.items():
            print(f"  {code}: {description}")

    def demo_callback_handling(self):
        """Demonstrate email callback handling."""
        print("\n" + "=" * 60)
        print("🔄 DEMO: Email Callback Handling")
        print("=" * 60)

        # Simulate callback data that would come from Nalo
        sample_callback = {
            "mid": "api.1.20220623.6FxcpucGNVXZhLeMj6euFS",
            "sender_address": "verified@yourdomain.com",
            "destination_address": "recipient@example.com",
            "timestamp": "2025-01-27 10:30:45",
            "status_desc": "sent",
        }

        print("Sample callback data:")
        print(f"  Email ID: {sample_callback['mid']}")
        print(f"  From: {sample_callback['sender_address']}")
        print(f"  To: {sample_callback['destination_address']}")
        print(f"  Time: {sample_callback['timestamp']}")
        print(f"  Status: {sample_callback['status_desc']}")

        # Handle the callback
        response = self.client.handle_email_callback(sample_callback)
        print(f"\n✅ Callback handled: {response}")

    def run_all_demos(self):
        """Run all email demonstrations."""
        print("🚀 Starting Comprehensive Nalo Solutions Email API Demo")
        print("=" * 80)

        # Run all demos
        self.demo_basic_email()
        self.demo_bulk_email()
        self.demo_html_email()
        self.demo_template_email()
        self.demo_email_with_attachment()
        self.demo_email_status_codes()
        self.demo_callback_handling()

        print("\n" + "=" * 80)
        print("✅ All email demos completed!")
        print("💡 Tips:")
        print("   - Make sure your sender email is verified in Nalo portal")
        print("   - Monitor your email balance for costs")
        print("   - Set up webhook endpoints for production callbacks")
        print("   - Use templates for consistent branding")
        print("=" * 80)


# Flask webhook example for email callbacks
def create_email_webhook_server():
    """Create a Flask server to handle email webhooks."""
    if not FLASK_AVAILABLE:
        raise ImportError(
            "Flask is required for webhook server. Install with: pip install flask"
        )

    app = Flask(__name__)

    @app.route("/webhooks/email-callback", methods=["POST"])
    def handle_email_callback():
        """Handle email delivery callback from Nalo Solutions."""
        try:
            callback_data = request.get_json()

            # Log the callback
            print("📧 Email Callback Received:")
            print(f"   Email ID: {callback_data.get('mid')}")
            print(f"   Status: {callback_data.get('status_desc')}")
            print(f"   Timestamp: {callback_data.get('timestamp')}")

            # Process with Nalo client
            client = load_nalo_client_from_env()
            response = client.handle_email_callback(callback_data)

            return jsonify(response), 200

        except Exception as e:
            print(f"❌ Error handling email callback: {e}")
            return jsonify({"error": "Callback processing failed"}), 500

    @app.route("/webhooks/bulk-email-callback", methods=["POST"])
    def handle_bulk_email_callback():
        """Handle bulk email delivery callbacks."""
        return handle_email_callback()  # Same logic for now

    @app.route("/webhooks/html-email-callback", methods=["POST"])
    def handle_html_email_callback():
        """Handle HTML email delivery callbacks."""
        return handle_email_callback()  # Same logic for now

    return app


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Nalo Solutions Email API Demo")
    parser.add_argument(
        "--webhook", action="store_true", help="Run webhook server instead of demos"
    )
    parser.add_argument(
        "--port", type=int, default=5000, help="Port for webhook server (default: 5000)"
    )

    args = parser.parse_args()

    if args.webhook:
        print("🌐 Starting Email Webhook Server...")
        app = create_email_webhook_server()
        app.run(host="0.0.0.0", port=args.port, debug=True)
    else:
        # Run email demos
        demo = EmailDemoApp()
        demo.run_all_demos()
