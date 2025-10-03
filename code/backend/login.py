import os
import secrets
import hashlib

# Simple storage
users = {}
sessions = {}

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
            
            # Find or create user
            user = next((u for u in users.values() if u['email'] == email), None)
            if not user:
                user_id = hashlib.sha256(f"{email}{secrets.token_hex(4)}".encode()).hexdigest()[:8]
                user = {'id': user_id, 'username': name, 'email': email}
                users[user_id] = user
            
            # Create session
            token = secrets.token_urlsafe(16)
            sessions[token] = user['id']
            
            return {'user': user, 'token': token}
    except:
        pass
    
    return None

def logout(token):
    """Logout function - removes session"""
    if token in sessions:
        del sessions[token]
        return True
    return False
