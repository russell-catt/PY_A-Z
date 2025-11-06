# GitLab API Key Setup

This project demonstrates how to securely add and use a GitLab API key with the Ross Video GitLab server.

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Create a GitLab API Key

1. Go to your GitLab account on https://srvottgitlabswitcher.rossvideo.com/
2. Navigate to your profile → **Preferences** → **Access Tokens**
3. Create a new token with a descriptive name
4. Select the scopes you need:
   - `api` - Full API access
   - `read_api` - Read-only API access
   - `read_user` - Read user information
   - `read_repository` - Read repository content
   - `write_repository` - Write repository content (if needed)
5. Click **Create personal access token**
6. Copy the generated token immediately (you'll only see it once!)

### 3. Configure the API Key

1. Copy the example environment file:
   ```bash
   cp env.template .env
   ```

2. Open `.env` and replace `your_gitlab_api_key_here` with your actual GitLab API key:
   ```
   GITLAB_API_KEY=glpat-xxxxxxxxxxxxxxxxxxxx
   GITLAB_URL=https://srvottgitlabswitcher.rossvideo.com/
   ```

   **Note:** The default GitLab URL is set to the Ross Video GitLab server. If you need to use a different instance, update `GITLAB_URL` accordingly.

### 4. Use the Configuration

Import the configuration in your Python code:

```python
from config import GITLAB_API_KEY, GITLAB_URL
import gitlab

# Initialize GitLab client
gl = gitlab.Gitlab(GITLAB_URL, private_token=GITLAB_API_KEY)

# Use the GitLab API
projects = gl.projects.list()
```

## Security Notes

- ✅ The `.env` file is in `.gitignore` to prevent committing secrets
- ✅ Never commit your API key to version control
- ✅ Use different API keys for different environments (dev, staging, production)
- ✅ Rotate your API keys regularly

## Example Usage

Run the example script:

```bash
python example_usage.py
```

## Validate Your API Key

Run the validation script to test your GitLab API key:

```bash
python validate_gitlab_key.py
```

This will:
- Check if your API key is configured correctly
- Test authentication with GitLab
- Verify API permissions and scopes
- Display your user information

## Alternative: Using Environment Variables Directly

If you prefer not to use a `.env` file, you can set environment variables directly:

**Windows PowerShell:**
```powershell
$env:GITLAB_API_KEY="your_key_here"
$env:GITLAB_URL="https://srvottgitlabswitcher.rossvideo.com/"
```

**Windows CMD:**
```cmd
set GITLAB_API_KEY=your_key_here
set GITLAB_URL=https://srvottgitlabswitcher.rossvideo.com/
```

**Linux/Mac:**
```bash
export GITLAB_API_KEY="your_key_here"
export GITLAB_URL="https://srvottgitlabswitcher.rossvideo.com/"
```

## GitLab Server

This configuration is set up for the Ross Video GitLab server:
- **URL:** https://srvottgitlabswitcher.rossvideo.com/

