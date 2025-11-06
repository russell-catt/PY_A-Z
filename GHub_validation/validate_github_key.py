"""
Script to validate GitHub API key configuration.
"""
import sys
from config import GITHUB_API_KEY, GITHUB_URL, validate_config
from github import Github
from github.GithubException import BadCredentialsException, GithubException

def validate_github_key():
    """Validate the GitHub API key by testing authentication."""
    print("=" * 60)
    print("GitHub API Key Validation")
    print("=" * 60)
    
    # Step 1: Check if configuration is loaded
    print("\n[1/3] Checking configuration...")
    try:
        validate_config()
        print(f"   [OK] Configuration loaded")
        print(f"   [OK] GitHub API URL: {GITHUB_URL}")
        print(f"   [OK] API Key: {GITHUB_API_KEY[:10]}...{GITHUB_API_KEY[-4:] if len(GITHUB_API_KEY) > 14 else '****'}")
        
        # Check if the token format looks like a GitHub token
        if GITHUB_API_KEY.startswith('glpat-'):
            print(f"   [WARNING] Token starts with 'glpat-' - this looks like a GitLab token, not a GitHub token!")
            print(f"            GitHub tokens typically start with 'ghp_' or 'github_pat_'.")
        elif not (GITHUB_API_KEY.startswith('ghp_') or GITHUB_API_KEY.startswith('github_pat_') or len(GITHUB_API_KEY) > 20):
            print(f"   [WARNING] Token format doesn't match typical GitHub token patterns.")
            print(f"            GitHub tokens usually start with 'ghp_' or 'github_pat_'.")
    except ValueError as e:
        print(f"   [ERROR] Configuration error: {e}")
        print("\n   Please ensure:")
        print("   1. A .env file exists in the project root")
        print("   2. GITHUB_API_KEY is set in the .env file")
        return False
    
    # Step 2: Test GitHub connection
    print("\n[2/3] Testing GitHub connection...")
    try:
        # Initialize GitHub client (use base_url for GitHub Enterprise)
        from github import Auth
        auth = Auth.Token(GITHUB_API_KEY)
        if GITHUB_URL != 'https://api.github.com':
            g = Github(base_url=GITHUB_URL, auth=auth)
        else:
            g = Github(auth=auth)
        # Test authentication by getting current user
        user = g.get_user()
        print(f"   [OK] Successfully connected to GitHub")
        print(f"   [OK] Authenticated as: {user.login} ({user.name or 'N/A'})")
        print(f"   [OK] User ID: {user.id}")
        print(f"   [OK] Email: {user.email or 'N/A (private)'}")
        print(f"   [OK] Public Repos: {user.public_repos}")
        print(f"   [OK] Followers: {user.followers}")
    except BadCredentialsException:
        print(f"   [ERROR] Authentication failed: Invalid API key")
        print("\n   Please check:")
        print("   1. Your API key is correct")
        print("   2. The API key hasn't expired")
        print("   3. The API key has the required permissions")
        return False
    except GithubException as e:
        if e.status == 401:
            print(f"   [ERROR] Authentication failed: {e}")
            return False
        elif e.status == 403:
            print(f"   [ERROR] Access forbidden: {e}")
            print("\n   This might indicate:")
            print("   1. Rate limit exceeded")
            print("   2. Insufficient permissions")
            return False
        else:
            print(f"   [ERROR] GitHub API error: {e}")
            return False
    except Exception as e:
        print(f"   [ERROR] Unexpected error: {type(e).__name__}: {e}")
        return False
    
    # Step 3: Test API permissions
    print("\n[3/3] Testing API permissions...")
    try:
        # Try to list repositories (requires repo scope)
        repos = user.get_repos()
        repo_count = sum(1 for _ in repos[:5])  # Count first 5
        print(f"   [OK] Can read repositories (repo scope working)")
        
        # Try to get rate limit info
        try:
            rate_limit = g.get_rate_limit()
            # Handle different versions of PyGithub
            if hasattr(rate_limit, 'core'):
                print(f"   [OK] API rate limit: {rate_limit.core.remaining}/{rate_limit.core.limit} remaining")
            elif hasattr(rate_limit, 'rate'):
                print(f"   [OK] API rate limit: {rate_limit.rate.remaining}/{rate_limit.rate.limit} remaining")
        except Exception:
            pass  # Rate limit info is optional
        
        print("\n" + "=" * 60)
        print("[SUCCESS] Validation successful! Your GitHub API key is working.")
        print("=" * 60)
        return True
    except GithubException as e:
        print(f"   [WARNING] Permission warning: {e}")
        print("\n   Your API key works but may be missing some permissions.")
        print("   Consider adding: repo, read:user, read:org")
        return True  # Still valid, just limited permissions
    except Exception as e:
        print(f"   [WARNING] Warning: {type(e).__name__}: {e}")
        return True  # Connection works, minor issue with permissions test

if __name__ == "__main__":
    success = validate_github_key()
    sys.exit(0 if success else 1)

