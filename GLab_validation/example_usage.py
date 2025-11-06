"""
Example usage of GitLab API with the configured API key.
"""
import gitlab
from config import GITLAB_API_KEY, GITLAB_URL, validate_config

def main():
    # Validate configuration
    validate_config()
    
    # Initialize GitLab client
    gl = gitlab.Gitlab(GITLAB_URL, private_token=GITLAB_API_KEY)
    
    # Test connection by getting current user
    try:
        user = gl.user
        print(f"Successfully connected to GitLab as: {user.username}")
        print(f"Name: {user.name}")
        print(f"Email: {getattr(user, 'email', 'N/A')}")
    except Exception as e:
        print(f"Error connecting to GitLab: {e}")
    
    # Example: List your projects
    try:
        projects = gl.projects.list(owned=True, get_all=True)
        print(f"\nFound {len(projects)} projects you own:")
        for project in projects[:5]:  # Show first 5
            print(f"  - {project.name}")
            print(f"    URL: {project.web_url}")
    except Exception as e:
        print(f"Error listing projects: {e}")

if __name__ == "__main__":
    main()

