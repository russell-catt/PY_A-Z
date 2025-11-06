"""
Example usage of Bluesky API with the configured credentials.
"""
from atproto import Client
from config import BLUESKY_HANDLE, BLUESKY_PASSWORD, BLUESKY_SERVICE, validate_config

def main():
    # Validate configuration
    validate_config()
    
    # Initialize Bluesky client
    client = Client(base_url=BLUESKY_SERVICE)
    
    # Login
    try:
        client.login(login=BLUESKY_HANDLE, password=BLUESKY_PASSWORD)
        print(f"Successfully connected to Bluesky as: {client.me.handle}")
        print(f"DID: {client.me.did}")
        print(f"Display Name: {getattr(client.me, 'display_name', 'N/A')}")
    except Exception as e:
        print(f"Error connecting to Bluesky: {e}")
        return
    
    # Example: Get your profile
    try:
        profile = client.get_profile(actor=BLUESKY_HANDLE)
        print(f"\nProfile Information:")
        print(f"  Handle: {profile.handle}")
        print(f"  Display Name: {profile.display_name or 'N/A'}")
        print(f"  Description: {profile.description or 'N/A'}")
        print(f"  Followers: {profile.followers_count}")
        print(f"  Following: {profile.follows_count}")
        print(f"  Posts: {profile.posts_count}")
    except Exception as e:
        print(f"Error getting profile: {e}")
    
    # Example: Get timeline
    try:
        timeline = client.get_timeline(limit=5)
        print(f"\nRecent Timeline Posts:")
        for feed_item in timeline.feed[:3]:
            post = feed_item.post
            print(f"  - {post.author.display_name or post.author.handle}: {post.record.text[:50]}...")
    except Exception as e:
        print(f"Error getting timeline: {e}")

if __name__ == "__main__":
    main()

