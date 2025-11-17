from flask import session, redirect, url_for
from authlib.integrations.flask_client import OAuth
import os

# Google OAuth configuration
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID', 'YOUR_GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET', 'YOUR_GOOGLE_CLIENT_SECRET')

# Check if OAuth is configured
OAUTH_CONFIGURED = (GOOGLE_CLIENT_ID != 'YOUR_GOOGLE_CLIENT_ID' and 
                    GOOGLE_CLIENT_SECRET != 'YOUR_GOOGLE_CLIENT_SECRET' and
                    GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET)

def init_oauth(app):
    """Initialize OAuth for the Flask app"""
    if not OAUTH_CONFIGURED:
        print("⚠️  WARNING: Google OAuth not configured. Using demo mode.")
        print("   To enable Google login, set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET environment variables.")
        return None
    
    oauth = OAuth(app)
    
    try:
        google = oauth.register(
            name='google',
            client_id=GOOGLE_CLIENT_ID,
            client_secret=GOOGLE_CLIENT_SECRET,
            server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
            client_kwargs={
                'scope': 'openid email profile'
            }
        )
        print("✅ Google OAuth configured successfully!")
        return google
    except Exception as e:
        print(f"⚠️  Error configuring OAuth: {e}")
        return None

def get_user_info():
    """Get user info from session"""
    return session.get('user', None)

def is_authenticated():
    """Check if user is authenticated"""
    return 'user' in session

