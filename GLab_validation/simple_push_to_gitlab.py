"""
Simplified script to push to GitLab - creates repo if needed, then pushes.
"""
import subprocess
import os
import sys
import gitlab
from config import GITLAB_API_KEY, GITLAB_URL, validate_config

def main():
    validate_config()
    repo_name = "GLab_validation"
    
    gl = gitlab.Gitlab(GITLAB_URL, private_token=GITLAB_API_KEY)
    
    try:
        # Get user info
        projects = gl.projects.list(per_page=1, get_all=False)
        if not projects:
            raise Exception("Could not authenticate")
        
        namespace = projects[0].namespace
        username = namespace.get('path', 'rcatt')
        print(f"Using namespace: {username}")
        
        # Check if repo exists
        full_path = f"{username}/{repo_name}"
        try:
            repo = gl.projects.get(full_path)
            print(f"Repository '{repo_name}' already exists.")
            repo_url = repo.http_url_to_repo
        except:
            # Create repo - use minimal required fields
            print(f"Creating repository '{repo_name}'...")
            repo = gl.projects.create({
                'name': repo_name,
                'visibility': 'private'
            })
            print(f"Repository created!")
            repo_url = repo.http_url_to_repo
        
        # Navigate to parent and push
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        os.chdir(parent_dir)
        
        # Remove existing gitlab remote
        subprocess.run(['git', 'remote', 'remove', 'gitlab'], 
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Add remote with token authentication
        repo_url_with_auth = repo_url.replace('https://', f'https://oauth2:{GITLAB_API_KEY}@')
        subprocess.run(['git', 'remote', 'add', 'gitlab', repo_url], check=True)
        print(f"Remote added: {repo_url}")
        
        # Configure git to use token
        repo_host = GITLAB_URL.replace('https://', '').replace('/', '')
        subprocess.run(['git', 'config', f'credential.https://{repo_host}.helper', 'store'], check=False)
        
        # Push using token in URL
        env = os.environ.copy()
        env['GIT_TERMINAL_PROMPT'] = '0'
        result = subprocess.run(
            ['git', 'push', '-u', 'gitlab', 'main'],
            input=f'oauth2:{GITLAB_API_KEY}\n'.encode(),
            env=env,
            check=False
        )
        
        if result.returncode != 0:
            # Try with credential helper
            print("Trying alternative push method...")
            repo_url_auth = repo_url.replace('https://', f'https://oauth2:{GITLAB_API_KEY}@')
            subprocess.run(['git', 'remote', 'set-url', 'gitlab', repo_url_auth], check=True)
            subprocess.run(['git', 'push', '-u', 'gitlab', 'main'], check=True)
        
        print(f"\nSuccessfully pushed to GitLab!")
        print(f"Repository: {repo_url}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

