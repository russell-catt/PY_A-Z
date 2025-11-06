"""
Example usage of GitHub API with the configured API key.
"""
from github import Github
from config import GITHUB_API_KEY, GITHUB_URL, validate_config

def main():
    # Validate configuration
    validate_config()
    
    # Initialize GitHub client (use base_url for GitHub Enterprise)
    from github import Auth
    auth = Auth.Token(GITHUB_API_KEY)
    if GITHUB_URL != 'https://api.github.com':
        g = Github(base_url=GITHUB_URL, auth=auth)
    else:
        g = Github(auth=auth)
    
    # Test connection by getting current user
    try:
        user = g.get_user()
        print(f"Successfully connected to GitHub as: {user.login}")
        print(f"Name: {user.name or 'N/A'}")
        print(f"Email: {user.email or 'N/A (private)'}")
    except Exception as e:
        print(f"Error connecting to GitHub: {e}")
    
    # Example: List your repositories
    try:
        repos = user.get_repos()
        print(f"\nFound repositories:")
        for repo in list(repos[:5]):  # Show first 5
            print(f"  - {repo.name} ({repo.private and 'private' or 'public'})")
            print(f"    URL: {repo.html_url}")
    except Exception as e:
        print(f"Error listing repositories: {e}")

if __name__ == "__main__":
    main()

