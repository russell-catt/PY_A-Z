# GitHub API Key Setup

This project demonstrates how to securely add and use a GitHub API key.

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Create a GitHub API Key

1. Go to your GitHub account settings
2. Navigate to **Developer settings** → **Personal access tokens** → **Tokens (classic)**
3. Click **Generate new token (classic)**
4. Give your token a descriptive name and select the scopes you need:
   - `repo` - Full control of private repositories
   - `read:user` - Read user profile information
   - `read:org` - Read org and team membership
   - `public_repo` - Access public repositories (if you only need public repos)
5. Click **Generate token**
6. Copy the generated token immediately (you'll only see it once!)

### 3. Configure the API Key

1. Copy the example environment file:
   ```bash
   cp env.template .env
   ```

2. Open `.env` and replace `your_github_api_key_here` with your actual GitHub API key:
   ```
   GITHUB_API_KEY=ghp_xxxxxxxxxxxxxxxxxxxx
   GITHUB_URL=https://api.github.com
   ```

   **Note:** If you're using GitHub Enterprise, update `GITHUB_URL` to your enterprise API endpoint (e.g., `https://github.yourcompany.com/api/v3`).

### 4. Use the Configuration

Import the configuration in your Python code:

```python
from config import GITHUB_API_KEY, GITHUB_URL
from github import Github

# Initialize GitHub client
g = Github(GITHUB_API_KEY)

# Use the GitHub API
user = g.get_user()
repos = user.get_repos()
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

Run the validation script to test your GitHub API key:

```bash
python validate_github_key.py
```

This will:
- Check if your API key is configured correctly
- Test authentication with GitHub
- Verify API permissions and scopes
- Display your user information

## Alternative: Using Environment Variables Directly

If you prefer not to use a `.env` file, you can set environment variables directly:

**Windows PowerShell:**
```powershell
$env:GITHUB_API_KEY="your_key_here"
$env:GITHUB_URL="https://api.github.com"
```

**Windows CMD:**
```cmd
set GITHUB_API_KEY=your_key_here
set GITHUB_URL=https://api.github.com
```

**Linux/Mac:**
```bash
export GITHUB_API_KEY="your_key_here"
export GITHUB_URL="https://api.github.com"
```

