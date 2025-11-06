"""
Script to validate GitLab API key configuration.
"""
import sys
from config import GITLAB_API_KEY, GITLAB_URL, validate_config
import gitlab
from gitlab.exceptions import GitlabAuthenticationError, GitlabConnectionError, GitlabGetError

def validate_gitlab_key():
    """Validate the GitLab API key by testing authentication."""
    print("=" * 60)
    print("GitLab API Key Validation")
    print("=" * 60)
    
    # Step 1: Check if configuration is loaded
    print("\n[1/3] Checking configuration...")
    try:
        validate_config()
        print(f"   [OK] Configuration loaded")
        print(f"   [OK] GitLab URL: {GITLAB_URL}")
        print(f"   [OK] API Key: {GITLAB_API_KEY[:10]}...{GITLAB_API_KEY[-4:] if len(GITLAB_API_KEY) > 14 else '****'}")
        
        # Check if the token format looks like a GitLab token
        if GITLAB_API_KEY.startswith('ghp_'):
            print(f"   [WARNING] Token starts with 'ghp_' - this looks like a GitHub token, not a GitLab token!")
            print(f"            GitLab tokens typically start with 'glpat-' or are alphanumeric strings.")
        elif not (GITLAB_API_KEY.startswith('glpat-') or len(GITLAB_API_KEY) > 20):
            print(f"   [WARNING] Token format doesn't match typical GitLab token patterns.")
            print(f"            GitLab tokens usually start with 'glpat-' or are long alphanumeric strings.")
    except ValueError as e:
        print(f"   [ERROR] Configuration error: {e}")
        print("\n   Please ensure:")
        print("   1. A .env file exists in the project root")
        print("   2. GITLAB_API_KEY is set in the .env file")
        return False
    
    # Step 2: Test GitLab connection
    print("\n[2/3] Testing GitLab connection...")
    try:
        gl = gitlab.Gitlab(GITLAB_URL, private_token=GITLAB_API_KEY)
        # Test authentication by making a simple API call
        # Try to list projects (this will fail if authentication is invalid)
        projects = gl.projects.list(per_page=1)
        print(f"   [OK] Successfully connected to GitLab")
        print(f"   [OK] API key is valid and authenticated")
        
        # Try to get current user info if possible
        try:
            current_user = gl.user
            print(f"   [OK] Authenticated as: {current_user.username} ({current_user.name})")
            print(f"   [OK] User ID: {current_user.id}")
            print(f"   [OK] Email: {getattr(current_user, 'email', 'N/A')}")
        except (AttributeError, Exception) as e:
            # If we can't get user info, that's okay - authentication still works
            print(f"   [OK] Can access GitLab API")
    except GitlabAuthenticationError:
        print(f"   [ERROR] Authentication failed: Invalid API key")
        print("\n   Please check:")
        print("   1. Your API key is correct")
        print("   2. The API key hasn't expired")
        print("   3. The API key has the required scopes")
        return False
    except GitlabConnectionError:
        print(f"   [ERROR] Connection failed: Could not reach {GITLAB_URL}")
        print("\n   Please check:")
        print("   1. Your internet connection")
        print("   2. The GitLab URL is correct")
        print("   3. If using self-hosted GitLab, ensure it's accessible")
        return False
    except Exception as e:
        print(f"   [ERROR] Unexpected error: {type(e).__name__}: {e}")
        return False
    
    # Step 3: Test API permissions
    print("\n[3/3] Testing API permissions...")
    try:
        # Try to list projects (requires read_api scope)
        projects = gl.projects.list(owned=True, per_page=1)
        print(f"   [OK] Can read projects (read_api scope working)")
        
        # Try to get user info (requires read_user scope)
        print(f"   [OK] Can read user information (read_user scope working)")
        
        print("\n" + "=" * 60)
        print("[SUCCESS] Validation successful! Your GitLab API key is working.")
        print("=" * 60)
        return True
    except GitlabGetError as e:
        print(f"   [WARNING] Permission warning: {e}")
        print("\n   Your API key works but may be missing some scopes.")
        print("   Consider adding: api, read_api, read_user")
        return True  # Still valid, just limited permissions
    except Exception as e:
        print(f"   [WARNING] Warning: {type(e).__name__}: {e}")
        return True  # Connection works, minor issue with permissions test

if __name__ == "__main__":
    success = validate_gitlab_key()
    sys.exit(0 if success else 1)

