#!/usr/bin/env python3
"""
Test script for USSD functionality with clean, generic implementation.
This demonstrates how to use the USSD API without payment processing.
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from nunyakata import NaloSolutions


def test_ussd_session():
    """Test USSD session flow."""
    print("🧪 Testing USSD Session Management...")

    # Initialize the client (no specific credentials needed for USSD demo)
    client = NaloSolutions(ussd_userid="NALOTest", ussd_environment="sandbox")

    # Test 1: Initial USSD request (MSGTYPE = true)
    print("\n1️⃣ Testing initial USSD request...")
    initial_request = {
        "USERID": "NALOTest",
        "MSISDN": "233265542141",
        "USERDATA": "*999#",  # Initial dial
        "MSGTYPE": True,  # Initial request
        "NETWORK": "MTN",
        "SESSIONID": "test_session_123",
    }

    response1 = client.handle_ussd_request(initial_request)
    print("Initial Response:")
    print(f"  USERID: {response1['USERID']}")
    print(f"  MSG: {response1['MSG']}")
    print(f"  MSGTYPE: {response1['MSGTYPE']}")

    # Test 2: Select menu option 1 (Check Balance)
    print("\n2️⃣ Testing menu selection (option 1)...")
    menu_request = {
        "USERID": "NALOTest",
        "MSISDN": "233265542141",
        "USERDATA": "1",  # Select option 1
        "MSGTYPE": False,  # Subsequent request
        "NETWORK": "MTN",
        "SESSIONID": "test_session_123",
    }

    response2 = client.handle_ussd_request(menu_request)
    print("Menu Response:")
    print(f"  MSG: {response2['MSG']}")
    print(f"  MSGTYPE: {response2['MSGTYPE']}")  # Should be False (session ends)

    # Test 3: Test sub-menu with option 3 (Services)
    print("\n3️⃣ Testing sub-menu navigation (option 3)...")

    # Start new session for sub-menu test
    initial_request_2 = {
        "USERID": "NALOTest",
        "MSISDN": "233265542141",
        "USERDATA": "*999#",
        "MSGTYPE": True,
        "NETWORK": "MTN",
        "SESSIONID": "test_session_456",
    }

    client.handle_ussd_request(initial_request_2)  # Initialize session

    # Select services menu
    services_request = {
        "USERID": "NALOTest",
        "MSISDN": "233265542141",
        "USERDATA": "3",  # Select option 3 (Services)
        "MSGTYPE": False,
        "NETWORK": "MTN",
        "SESSIONID": "test_session_456",
    }

    response3 = client.handle_ussd_request(services_request)
    print("Services Menu Response:")
    print(f"  MSG: {response3['MSG']}")
    print(f"  MSGTYPE: {response3['MSGTYPE']}")  # Should be True (continue session)

    # Test 4: Select a service option
    print("\n4️⃣ Testing service selection...")
    service_selection = {
        "USERID": "NALOTest",
        "MSISDN": "233265542141",
        "USERDATA": "1",  # Select Service A
        "MSGTYPE": False,
        "NETWORK": "MTN",
        "SESSIONID": "test_session_456",
    }

    response4 = client.handle_ussd_request(service_selection)
    print("Service Selection Response:")
    print(f"  MSG: {response4['MSG']}")
    print(f"  MSGTYPE: {response4['MSGTYPE']}")  # Should be False (session ends)

    # Test 5: Test session management
    print("\n5️⃣ Testing session management...")
    print(f"Active sessions: {len(client._ussd_sessions)}")

    # Test session cleanup
    client.clear_ussd_session("test_session_123")
    client.clear_ussd_session("test_session_456")
    print(f"After cleanup: {len(client._ussd_sessions)} sessions")

    print("\n✅ USSD testing completed!")


def test_ussd_utilities():
    """Test USSD utility functions."""
    print("\n🧪 Testing USSD Utilities...")

    client = NaloSolutions()

    # Test phone number validation
    print("\n📞 Testing phone number validation...")
    test_numbers = [
        "0265542141",  # Valid local format
        "233265542141",  # Valid international format
        "026554214",  # Invalid (too short)
        "02655421411",  # Invalid (too long)
        "1234567890",  # Invalid (wrong pattern)
        "",  # Invalid (empty)
    ]

    for number in test_numbers:
        is_valid = client.validate_phone_number(number)
        print(f"  {number:15} -> {'✅ Valid' if is_valid else '❌ Invalid'}")

    # Test amount validation
    print("\n💰 Testing amount validation...")
    test_amounts = [
        "10.50",  # Valid
        "100",  # Valid
        "0.99",  # Valid
        "10.123",  # Invalid (too many decimals)
        "-5.00",  # Invalid (negative)
        "0",  # Invalid (zero)
        "abc",  # Invalid (not a number)
        "",  # Invalid (empty)
    ]

    for amount in test_amounts:
        is_valid = client.validate_amount(amount)
        print(f"  {amount:10} -> {'✅ Valid' if is_valid else '❌ Invalid'}")

    # Test menu creation
    print("\n📋 Testing menu creation...")
    menu = client.create_ussd_menu(
        "Test Menu", ["Option A", "Option B", "Option C"], "0. Back"
    )
    print("Generated menu:")
    print(menu)

    print("\n✅ Utility testing completed!")


def demonstrate_custom_implementation():
    """Demonstrate how to extend the USSD class for custom business logic."""
    print("\n🧪 Demonstrating Custom USSD Implementation...")

    class CustomUSSD(NaloSolutions):
        """Custom USSD implementation with business-specific logic."""

        def _handle_service_menu(
            self,
            userid: str,
            msisdn: str,
            userdata: str,
            network: str,
            sessionid: str,
            service: str,
        ) -> dict:
            """Override to implement custom business logic."""
            if service == "services":
                try:
                    selection = int(userdata.strip())
                    if selection == 1:
                        # Custom Service A logic
                        msg = f"Welcome {msisdn}!\nYou selected Service A.\nYour network: {network}\nCustom logic goes here!"
                    elif selection == 2:
                        # Custom Service B logic
                        msg = f"Service B activated for {msisdn}.\nNetwork: {network}\nImplement your logic here!"
                    elif selection == 3:
                        # Custom Service C logic
                        msg = "Service C - Advanced Features\nThis could trigger payment, SMS, or other integrations."
                    else:
                        msg = "Invalid selection. Please choose 1-3."

                    return self._create_nalo_ussd_response(
                        userid, msisdn, userdata, msg, False
                    )
                except ValueError:
                    msg = "Please enter a valid number (1-3)."
                    return self._create_nalo_ussd_response(
                        userid, msisdn, userdata, msg, False
                    )
            else:
                # Call parent implementation for other services
                return super()._handle_service_menu(
                    userid, msisdn, userdata, network, sessionid, service
                )

    # Test custom implementation
    custom_client = CustomUSSD(ussd_userid="CustomDemo")

    # Initialize session
    init_request = {
        "USERID": "CustomDemo",
        "MSISDN": "233265542141",
        "USERDATA": "*999#",
        "MSGTYPE": True,
        "NETWORK": "VODAFONE",
        "SESSIONID": "custom_session_789",
    }

    custom_client.handle_ussd_request(init_request)

    # Navigate to services
    services_request = {
        "USERID": "CustomDemo",
        "MSISDN": "233265542141",
        "USERDATA": "3",
        "MSGTYPE": False,
        "NETWORK": "VODAFONE",
        "SESSIONID": "custom_session_789",
    }

    services_response = custom_client.handle_ussd_request(services_request)
    print("Custom Services Menu:")
    print(f"  MSG: {services_response['MSG']}")

    # Select custom service
    custom_service_request = {
        "USERID": "CustomDemo",
        "MSISDN": "233265542141",
        "USERDATA": "1",
        "MSGTYPE": False,
        "NETWORK": "VODAFONE",
        "SESSIONID": "custom_session_789",
    }

    custom_response = custom_client.handle_ussd_request(custom_service_request)
    print("\nCustom Service Response:")
    print(f"  MSG: {custom_response['MSG']}")

    print("\n✅ Custom implementation demo completed!")


if __name__ == "__main__":
    print("🚀 USSD Implementation Test Suite")
    print("=" * 50)

    try:
        test_ussd_session()
        test_ussd_utilities()
        demonstrate_custom_implementation()

        print("\n🎉 All tests completed successfully!")
        print("\n📝 Implementation Notes:")
        print("• The USSD implementation follows Nalo API format")
        print("• Sessions are managed automatically")
        print("• Validation methods are provided for common inputs")
        print("• Override _handle_service_menu() for custom business logic")
        print("• No payment processing - implement separately as needed")

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback

        traceback.print_exc()
