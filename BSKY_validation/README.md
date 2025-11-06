# Bluesky API Key Setup

This project demonstrates how to securely add and use Bluesky API credentials (handle and app password) for the account @sallocat.bsky.social.

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Create a Bluesky App Password

**Important:** Bluesky uses App Passwords, not your regular account password!

1. Go to your Bluesky account settings: https://bsky.app/settings/app-passwords
2. Click **Add App Password**
3. Give it a descriptive name (e.g., "Python API Access")
4. Click **Generate App Password**
5. **Copy the generated password immediately** - you'll only see it once!
6. The password will look something like: `xxxx-xxxx-xxxx-xxxx`

**Note:** App passwords are different from your regular Bluesky password. You cannot use your regular password for API access.

### 3. Configure the Credentials

1. Copy the example environment file:
   ```bash
   cp env.template .env
   ```

2. Open `.env` and replace `your_app_password_here` with your actual Bluesky app password:
   ```
   BLUESKY_HANDLE=sallocat.bsky.social
   BLUESKY_PASSWORD=xxxx-xxxx-xxxx-xxxx
   BLUESKY_SERVICE=https://bsky.social
   ```

   **Note:** The default handle is set to `sallocat.bsky.social`. If you need to use a different account, update `BLUESKY_HANDLE` accordingly.

### 4. Use the Configuration

Import the configuration in your Python code:

```python
from config import BLUESKY_HANDLE, BLUESKY_PASSWORD, BLUESKY_SERVICE
from atproto import Client

# Initialize Bluesky client
client = Client(base_url=BLUESKY_SERVICE)

# Login
client.login(login=BLUESKY_HANDLE, password=BLUESKY_PASSWORD)

# Use the Bluesky API
profile = client.get_profile(actor=BLUESKY_HANDLE)
timeline = client.get_timeline(limit=10)
```

## Security Notes

- ✅ The `.env` file is in `.gitignore` to prevent committing secrets
- ✅ Never commit your app password to version control
- ✅ App passwords can be revoked and recreated at any time
- ✅ Use different app passwords for different applications
- ✅ Revoke app passwords you no longer need

## Example Usage

Run the example script:

```bash
python example_usage.py
```

## Validate Your Credentials

Run the validation script to test your Bluesky credentials:

```bash
python validate_bluesky_key.py
```

This will:
- Check if your credentials are configured correctly
- Test authentication with Bluesky
- Verify API permissions
- Display your account information

## Alternative: Using Environment Variables Directly

If you prefer not to use a `.env` file, you can set environment variables directly:

**Windows PowerShell:**
```powershell
$env:BLUESKY_HANDLE="sallocat.bsky.social"
$env:BLUESKY_PASSWORD="your_app_password_here"
$env:BLUESKY_SERVICE="https://bsky.social"
```

**Windows CMD:**
```cmd
set BLUESKY_HANDLE=sallocat.bsky.social
set BLUESKY_PASSWORD=your_app_password_here
set BLUESKY_SERVICE=https://bsky.social
```

**Linux/Mac:**
```bash
export BLUESKY_HANDLE="sallocat.bsky.social"
export BLUESKY_PASSWORD="your_app_password_here"
export BLUESKY_SERVICE="https://bsky.social"
```

## Bluesky Account

This configuration is set up for the Bluesky account:
- **Handle:** @sallocat.bsky.social

## Troubleshooting

### "Invalid identifier or password" Error

- Make sure you're using an **App Password**, not your regular password
- Verify the handle is correct (must include `.bsky.social`)
- Check that the app password hasn't been revoked

### "Connection failed" Error

- Check your internet connection
- Verify the Bluesky service is accessible
- Try visiting https://bsky.social in your browser

### Creating App Passwords

If you need to create a new app password:
1. Go to: https://bsky.app/settings/app-passwords
2. Click "Add App Password"
3. Give it a name and generate
4. Copy it immediately (you'll only see it once!)

