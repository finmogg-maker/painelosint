# Google OAuth Setup Guide

## Step 1: Create Google OAuth Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google+ API
4. Go to "Credentials" → "Create Credentials" → "OAuth client ID"
5. Choose "Web application"
6. Add authorized redirect URI: `http://localhost:5000/auth/callback`
7. Copy the Client ID and Client Secret

## Step 2: Set Environment Variables

### Windows (PowerShell):
```powershell
$env:GOOGLE_CLIENT_ID="your_client_id_here"
$env:GOOGLE_CLIENT_SECRET="your_client_secret_here"
$env:SECRET_KEY="your_secret_key_here"
```

### Windows (Command Prompt):
```cmd
set GOOGLE_CLIENT_ID=your_client_id_here
set GOOGLE_CLIENT_SECRET=your_client_secret_here
set SECRET_KEY=your_secret_key_here
```

### Linux/Mac:
```bash
export GOOGLE_CLIENT_ID="your_client_id_here"
export GOOGLE_CLIENT_SECRET="your_client_secret_here"
export SECRET_KEY="your_secret_key_here"
```

## Step 3: Update auth.py (Optional)

You can also directly edit `auth.py` and replace:
- `YOUR_GOOGLE_CLIENT_ID` with your actual Client ID
- `YOUR_GOOGLE_CLIENT_SECRET` with your actual Client Secret

## Step 4: Run the Application

```bash
python app.py
```

The application will now support Google OAuth login!

## Notes

- For production, use environment variables instead of hardcoding credentials
- Update the redirect URI in Google Cloud Console to match your production domain
- The SECRET_KEY is used for Flask session encryption

