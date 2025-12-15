"""
Script to create a GitLab repository and push the code.
"""
import subprocess
import os
import sys
import gitlab
from config import GITLAB_API_KEY, GITLAB_URL, validate_config

def main():
    # Validate configuration
    try:
        validate_config()
    except ValueError as e:
        print(f"Configuration error: {e}")
        print("Please ensure GITLAB_API_KEY is set in your .env file")
        sys.exit(1)
    
    # Get repository name
    repo_name = "GLab_validation"
    
    # Initialize GitLab client
    gl = gitlab.Gitlab(GITLAB_URL, private_token=GITLAB_API_KEY)
    
    try:
        # Get current user - try different methods
        user = None
        try:
            user = gl.user
        except:
            pass
        
        if not user:
            # Try to get user from a project's namespace
            projects = gl.projects.list(per_page=1, get_all=False)
            if projects and projects[0].namespace:
                namespace = projects[0].namespace
                username = namespace.get('path', 'user')
                user_id = namespace.get('id')
                print(f"Authenticated as: {username} (ID: {user_id})")
            else:
                raise Exception("Could not authenticate - please check your API key")
        else:
            username = user.username
            user_id = user.id
            print(f"Authenticated as: {username} (ID: {user_id})")
        
        # Check if repository already exists
        print(f"Checking if repository '{repo_name}' exists...")
        projects = gl.projects.list(search=repo_name, owned=True, get_all=True)
        existing_repo = None
        for proj in projects:
            if proj.name == repo_name:
                existing_repo = proj
                break
        
        if existing_repo:
            print(f"Repository '{repo_name}' already exists.")
            repo_url = existing_repo.http_url_to_repo
        else:
            # Create new repository
            print(f"Creating repository '{repo_name}' on GitLab...")
            # Try creating with namespace path instead of namespace_id
            try:
                repo = gl.projects.create({
                    'name': repo_name,
                    'path': repo_name.lower().replace('_', '-'),
                    'description': 'GitLab API key setup and validation',
                    'visibility': 'private',
                    'namespace': username  # Use namespace path instead of ID
                })
            except:
                # Fallback: try without namespace (uses user's default namespace)
                repo = gl.projects.create({
                    'name': repo_name,
                    'path': repo_name.lower().replace('_', '-'),
                    'description': 'GitLab API key setup and validation',
                    'visibility': 'private'
                })
            print(f"Repository '{repo_name}' created successfully!")
            repo_url = repo.http_url_to_repo
        
        # Navigate to parent directory to work with git
        parent_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(os.path.dirname(parent_dir))
        
        # Add GitLab remote (remove existing gitlab remote if it exists)
        try:
            subprocess.run(['git', 'remote', 'remove', 'gitlab'], 
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except:
            pass
        
        # Add GitLab remote
        subprocess.run(['git', 'remote', 'add', 'gitlab', repo_url], check=True)
        print(f"Remote 'gitlab' added: {repo_url}")
        
        # Push to GitLab
        print(f"\nPushing to GitLab...")
        subprocess.run(['git', 'push', '-u', 'gitlab', 'main'], check=True)
        print(f"\nSuccessfully pushed to GitLab!")
        print(f"Repository URL: {repo_url}")
        
    except subprocess.CalledProcessError as e:
        print(f"Error during git operations: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
