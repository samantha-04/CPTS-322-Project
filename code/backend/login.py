import os
import secrets
import hashlib
from typing import Optional, Dict, Any

# Use SQLite-backed db module for persistent user storage
from . import db

# sessions remain in-memory tokens mapped to user id; db also stores sessions for persistence
sessions: Dict[str, str] = {}


# Load persistent sessions into memory at import time
try:
    persisted = db.get_all_sessions()
    sessions.update(persisted)
except Exception:
    # if DB isn't ready yet, ignore; functions will create sessions on demand
    pass


def create_session_for_user(user_id: str) -> str:
    """Create a session token for user_id, persist it, and return token."""
    token = secrets.token_urlsafe(16)
    sessions[token] = user_id
    try:
        db.create_session(token, user_id)
    except Exception:
        # ignore DB errors for now
        pass
    return token


def get_user_by_session(token: str) -> Optional[Dict[str, Any]]:
    """Return user object for a session token or None."""
    user_id = sessions.get(token) or db.get_user_id_by_session(token)
    if not user_id:
        return None
    return db.get_user_by_id(user_id)


def authenticate_password(email: str, password: str) -> Optional[Dict[str, Any]]:
    """Verify password and create session; returns {'user','token'} on success."""
    user = db.get_user_by_email(email)
    if not user or not user.get('salt') or not user.get('pwd_hash'):
        return None
    if db.verify_password(user['salt'], user['pwd_hash'], password):
        token = create_session_for_user(user['id'])
        return {'user': user, 'token': token}
    return None

# I think that this also handles new user creation
def login(app, redirect_uri=None):
    """Login function - handles both OAuth start and callback"""
    from flask import request
    from authlib.integrations.flask_client import OAuth
    
    oauth = OAuth(app)
    google = oauth.register(
        name='google',
        client_id=os.getenv('GOOGLE_CLIENT_ID'),
        client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
        server_metadata_url='https://accounts.google.com/.well-known/openid_configuration',
        client_kwargs={'scope': 'openid email profile'}
    )
    
    # If no code parameter, start OAuth flow
    if not request.args.get('code'):
        return google.authorize_redirect(redirect_uri or 'http://localhost:5000/login')
    
    # Handle callback
    try:
        token = google.authorize_access_token()
        resp = google.parse_id_token(token)
        
        if resp:
            email = resp.get('email')
            name = resp.get('name')
            
            # Find or create user via DB
            user = db.get_user_by_email(email)
            if not user:
                user = db.create_user_oauth(name, email)

            # Create session (in-memory and persistent)
            token = secrets.token_urlsafe(16)
            sessions[token] = user['id']
            db.create_session(token, user['id'])

            return {'user': user, 'token': token}
    except:
        pass
    
    return None

def logout(token: str) -> bool:
    """Logout function - removes session (in-memory and DB)"""
    if token in sessions:
        del sessions[token]
    db.delete_session(token)
    return True
