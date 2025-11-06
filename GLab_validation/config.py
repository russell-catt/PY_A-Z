"""
Configuration module for loading environment variables.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# GitLab configuration
GITLAB_API_KEY = os.getenv('GITLAB_API_KEY')
GITLAB_URL = os.getenv('GITLAB_URL', 'https://srvottgitlabswitcher.rossvideo.com/')

def validate_config():
    """Validate that required configuration is present."""
    if not GITLAB_API_KEY:
        raise ValueError(
            "GITLAB_API_KEY not found in environment variables. "
            "Please create a .env file with your GitLab API key."
        )
    return True

