#!/usr/bin/env python3
"""
Test script to verify VAPI API call format
This script demonstrates the correct format for VAPI API calls
"""

import json

def format_phone_for_vapi(phone_str):
    """Clean and format phone number for VAPI API"""
    # Remove all non-digit characters
    clean_phone = ''.join(filter(str.isdigit, phone_str))
    
    # Add country code if not present (assuming US numbers)
    if len(clean_phone) == 10:
        clean_phone = "1" + clean_phone
    elif len(clean_phone) == 11 and clean_phone.startswith("1"):
        pass  # Already has country code
    else:
        # Invalid phone number length
        return None
    
    # Format as +1XXXXXXXXXX
    return f"+{clean_phone}"

def create_vapi_payload(phone, assistant_id, metadata=None):
    """Create properly formatted VAPI API payload"""
    formatted_phone = format_phone_for_vapi(phone)
    
    if not formatted_phone:
        raise ValueError(f"Invalid phone number format: {phone}")
    
    payload = {
        "phoneNumber": {
            "twilioPhoneNumber": formatted_phone
        },
        "assistantId": assistant_id
    }
    
    if metadata:
        payload["metadata"] = metadata
    
    return payload

# Test with sample data
if __name__ == "__main__":
    print("VAPI API Call Format Test")
    print("=" * 40)
    
    # Test phone numbers
    test_phones = [
        "555-676-8585",
        "555-787-9696", 
        "(555) 898-0707",
        "555.909.1818",
        "5550102929"
    ]
    
    assistant_id = "your-assistant-id-here"
    
    for phone in test_phones:
        try:
            payload = create_vapi_payload(
                phone=phone,
                assistant_id=assistant_id,
                metadata={
                    "lead_name": "Test Customer",
                    "email": "test@example.com",
                    "order_id": "ORD001"
                }
            )
            
            print(f"\nPhone: {phone}")
            print(f"Formatted: {format_phone_for_vapi(phone)}")
            print("Payload:")
            print(json.dumps(payload, indent=2))
            print("-" * 30)
            
        except ValueError as e:
            print(f"\nPhone: {phone}")
            print(f"Error: {e}")
            print("-" * 30)
    
    print("\nKey Changes Made:")
    print("1. phoneNumber is now an object with 'twilioPhoneNumber' field")
    print("2. Changed 'agent' to 'assistantId'")
    print("3. Phone numbers are formatted as +1XXXXXXXXXX")
    print("4. All non-digit characters are removed from phone numbers")
    print("5. US country code (+1) is automatically added if missing")

