"""
Script to validate Bluesky API credentials (handle and app password).
"""
import sys
from config import BLUESKY_HANDLE, BLUESKY_PASSWORD, BLUESKY_SERVICE, validate_config
from atproto import Client

def validate_bluesky_key():
    """Validate the Bluesky credentials by testing authentication."""
    print("=" * 60)
    print("Bluesky API Credentials Validation")
    print("=" * 60)
    
    # Step 1: Check if configuration is loaded
    print("\n[1/3] Checking configuration...")
    try:
        validate_config()
        print(f"   [OK] Configuration loaded")
        print(f"   [OK] Bluesky Handle: {BLUESKY_HANDLE}")
        print(f"   [OK] Bluesky Service: {BLUESKY_SERVICE}")
        print(f"   [OK] App Password: {'*' * 10}...{BLUESKY_PASSWORD[-4:] if len(BLUESKY_PASSWORD) > 14 else '****'}")
        
        if not BLUESKY_HANDLE.endswith('.bsky.social'):
            print(f"   [WARNING] Handle doesn't end with '.bsky.social' - ensure it's correct")
    except ValueError as e:
        print(f"   [ERROR] Configuration error: {e}")
        print("\n   Please ensure:")
        print("   1. A .env file exists in the project root")
        print("   2. BLUESKY_PASSWORD is set in the .env file")
        print("   3. BLUESKY_HANDLE is set (default: sallocat.bsky.social)")
        return False
    
    # Step 2: Test Bluesky connection
    print("\n[2/3] Testing Bluesky connection...")
    try:
        client = Client(base_url=BLUESKY_SERVICE)
        # Login with handle and app password
        client.login(login=BLUESKY_HANDLE, password=BLUESKY_PASSWORD)
        print(f"   [OK] Successfully connected to Bluesky")
        print(f"   [OK] Authenticated as: {client.me.handle}")
        print(f"   [OK] DID: {client.me.did}")
        print(f"   [OK] Display Name: {getattr(client.me, 'display_name', 'N/A')}")
    except Exception as e:
        error_msg = str(e)
        if 'Invalid identifier or password' in error_msg or '401' in error_msg:
            print(f"   [ERROR] Authentication failed: Invalid handle or app password")
            print("\n   Please check:")
            print("   1. Your Bluesky handle is correct (e.g., sallocat.bsky.social)")
            print("   2. You're using an App Password, not your regular password")
            print("   3. The app password hasn't been revoked")
            print("\n   To create an App Password:")
            print("   1. Go to https://bsky.app/settings/app-passwords")
            print("   2. Create a new app password")
            print("   3. Copy it immediately (you'll only see it once!)")
            return False
        elif 'Connection' in error_msg or 'Network' in error_msg:
            print(f"   [ERROR] Connection failed: Could not reach Bluesky")
            print("\n   Please check:")
            print("   1. Your internet connection")
            print("   2. The Bluesky service is accessible")
            return False
        else:
            print(f"   [ERROR] Unexpected error: {type(e).__name__}: {e}")
            return False
    
    # Step 3: Test API permissions
    print("\n[3/3] Testing API permissions...")
    try:
        # Try to get profile information
        profile = client.get_profile(actor=BLUESKY_HANDLE)
        print(f"   [OK] Can read profile information")
        
        # Try to get timeline (requires read permissions)
        timeline = client.get_timeline(limit=1)
        print(f"   [OK] Can read timeline (read permissions working)")
        
        print("\n" + "=" * 60)
        print("[SUCCESS] Validation successful! Your Bluesky credentials are working.")
        print("=" * 60)
        return True
    except Exception as e:
        print(f"   [WARNING] Permission warning: {type(e).__name__}: {e}")
        print("\n   Your credentials work but may have limited permissions.")
        return True  # Still valid, just limited permissions

if __name__ == "__main__":
    success = validate_bluesky_key()
    sys.exit(0 if success else 1)

