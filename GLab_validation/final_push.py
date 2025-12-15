"""
Final script to create GitLab repo and push code.
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
        # Get user's namespace
        user = gl.user
        if not user:
            # Fallback: get from projects
            projects = gl.projects.list(per_page=1, get_all=False)
            if not projects:
                raise Exception("Could not authenticate")
            namespace_id = projects[0].namespace['id']
        else:
            # Get user's namespace ID
            namespaces = gl.namespaces.list(search=user.username, get_all=False)
            if namespaces:
                namespace_id = namespaces[0].id
            else:
                namespace_id = user.id  # Use user ID as namespace
        
        print(f"Using namespace ID: {namespace_id}")
        
        # Check if repo exists
        try:
            repo = gl.projects.get(f"{user.username if user else 'rcatt'}/{repo_name}")
            print(f"Repository exists: {repo.web_url}")
            repo_url = repo.http_url_to_repo
        except:
            # Create repo
            print(f"Creating repository '{repo_name}'...")
            repo = gl.projects.create({
                'name': repo_name,
                'namespace_id': namespace_id,
                'visibility': 'private'
            })
            print(f"Repository created: {repo.web_url}")
            repo_url = repo.http_url_to_repo
        
        # Push to GitLab
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        os.chdir(parent_dir)
        
        # Remove and re-add remote with auth
        subprocess.run(['git', 'remote', 'remove', 'gitlab'], 
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        repo_url_auth = repo_url.replace('https://', f'https://oauth2:{GITLAB_API_KEY}@')
        subprocess.run(['git', 'remote', 'add', 'gitlab', repo_url_auth], check=True)
        
        print(f"Pushing to GitLab...")
        subprocess.run(['git', 'push', '-u', 'gitlab', 'main'], check=True)
        
        print(f"\nSuccessfully pushed to GitLab!")
        print(f"Repository: {repo.web_url}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

