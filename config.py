"""
Configuration module for loading environment variables.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# GitHub configuration
GITHUB_API_KEY = os.getenv('GITHUB_API_KEY')
GITHUB_URL = os.getenv('GITHUB_URL', 'https://api.github.com')

def validate_config():
    """Validate that required configuration is present."""
    if not GITHUB_API_KEY:
        raise ValueError(
            "GITHUB_API_KEY not found in environment variables. "
            "Please create a .env file with your GitHub API key."
        )
    return True

