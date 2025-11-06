"""
Configuration module for loading environment variables.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Bluesky configuration
BLUESKY_HANDLE = os.getenv('BLUESKY_HANDLE', 'sallocat.bsky.social')
BLUESKY_PASSWORD = os.getenv('BLUESKY_PASSWORD')  # App password, not regular password
BLUESKY_SERVICE = os.getenv('BLUESKY_SERVICE', 'https://bsky.social')

def validate_config():
    """Validate that required configuration is present."""
    if not BLUESKY_PASSWORD:
        raise ValueError(
            "BLUESKY_PASSWORD not found in environment variables. "
            "Please create a .env file with your Bluesky app password."
        )
    return True

