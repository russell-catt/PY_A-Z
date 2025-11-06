"""
Script to publish a post to Bluesky.
"""
from atproto import Client
from config import BLUESKY_HANDLE, BLUESKY_PASSWORD, BLUESKY_SERVICE, validate_config

def publish_post():
    """Publish a post to Bluesky."""
    # Validate configuration
    try:
        validate_config()
        print("Configuration validated successfully.")
    except ValueError as e:
        print(f"Configuration error: {e}")
        print("Please ensure BLUESKY_PASSWORD is set in your .env file")
        return False
    
    # Initialize Bluesky client
    client = Client(base_url=BLUESKY_SERVICE)
    
    try:
        # Login
        print(f"Connecting to Bluesky as {BLUESKY_HANDLE}...")
        client.login(login=BLUESKY_HANDLE, password=BLUESKY_PASSWORD)
        print(f"Successfully authenticated as: {client.me.handle}")
        
        # Message to post
        message = "Hello World! I made this message with Python and Cursor."
        
        # Publish the post
        print(f"\nPublishing post: '{message}'")
        from atproto import models
        
        # Create the post record
        post_record = models.AppBskyFeedPost.Record(
            text=message,
            created_at=client.get_current_time_iso()
        )
        
        # Create the post using the repo API with data parameter
        response = client.com.atproto.repo.create_record(
            data=models.ComAtprotoRepoCreateRecord.Data(
                repo=client.me.did,
                collection=models.ids.AppBskyFeedPost,
                record=post_record
            )
        )
        
        print(f"\n[SUCCESS] Post published successfully!")
        print(f"Post URI: {response.uri}")
        print(f"Post CID: {response.cid}")
        print(f"\nView your post at: https://bsky.app/profile/{BLUESKY_HANDLE}")
        
        return True
        
    except Exception as e:
        error_msg = str(e)
        if 'Invalid identifier or password' in error_msg or '401' in error_msg:
            print(f"\n[ERROR] Authentication failed: Invalid handle or app password")
            print("\nPlease check:")
            print("1. Your Bluesky handle is correct")
            print("2. You're using an App Password, not your regular password")
            print("3. The app password hasn't been revoked")
        elif 'Connection' in error_msg or 'Network' in error_msg:
            print(f"\n[ERROR] Connection failed: Could not reach Bluesky")
            print("Please check your internet connection")
        else:
            print(f"\n[ERROR] Failed to publish post: {type(e).__name__}: {e}")
        return False

if __name__ == "__main__":
    success = publish_post()
    exit(0 if success else 1)

