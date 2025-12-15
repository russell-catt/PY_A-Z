"""
Create GitLab repository and push code - using namespace path.
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
        
        # Try to get existing repo
        full_path = f"{username}/{repo_name}"
        try:
            repo = gl.projects.get(full_path)
            print(f"Repository exists: {repo.web_url}")
            repo_url = repo.http_url_to_repo
        except:
            # Create repo - try without namespace (uses user's default)
            print(f"Creating repository '{repo_name}'...")
            try:
                # Try with just name and path
                repo = gl.projects.create({
                    'name': repo_name,
                    'path': repo_name.lower().replace('_', '-'),
                    'visibility': 'private'
                })
            except Exception as e1:
                print(f"First attempt failed: {e1}")
                # Try with minimal fields
                try:
                    repo = gl.projects.create({
                        'name': repo_name,
                        'visibility': 'private'
                    })
                except Exception as e2:
                    print(f"Second attempt failed: {e2}")
                    print("\nPlease create the repository manually on GitLab:")
                    print(f"  1. Go to {GITLAB_URL}")
                    print(f"  2. Click 'New project'")
                    print(f"  3. Name it: {repo_name}")
                    print(f"  4. Set visibility to Private")
                    print(f"  5. Then run: git push -u gitlab main")
                    sys.exit(1)
            
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
        
        print(f"\nPushing to GitLab...")
        subprocess.run(['git', 'push', '-u', 'gitlab', 'main'], check=True)
        
        print(f"\nSuccessfully pushed to GitLab!")
        print(f"Repository: {repo.web_url}")
        
    except subprocess.CalledProcessError as e:
        print(f"\nGit push failed. Please ensure the repository exists on GitLab.")
        print(f"If it doesn't exist, create it manually at: {GITLAB_URL}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

