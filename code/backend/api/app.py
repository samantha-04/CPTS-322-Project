from flask import Flask, jsonify, request
from flask_cors import CORS

# backend helpers
from .. import login
from .. import db

app = Flask(__name__)
CORS(app)

@app.route('/health')
def hello():
    return jsonify({'status': 200, 'message': 'API is live'})


@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json(force=True)
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    if not username or not email or not password:
        return jsonify({'error': 'missing_fields'}), 400
    existing = db.get_user_by_email(email)
    if existing:
        return jsonify({'error': 'email_exists'}), 400
    user = db.create_user_with_password_plain(username, email, password)
    # hide sensitive fields
    user.pop('salt', None)
    user.pop('pwd_hash', None)
    return jsonify({'user': user}), 201


@app.route('/login/password', methods=['POST'])
def login_password():
    data = request.get_json(force=True)
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({'error': 'missing_fields'}), 400
    auth = login.authenticate_password(email, password)
    if not auth:
        return jsonify({'error': 'invalid_credentials'}), 401
    user = auth['user']
    token = auth['token']
    user.pop('salt', None)
    user.pop('pwd_hash', None)
    return jsonify({'user': user, 'token': token})


@app.route('/logout', methods=['POST'])
def logout():
    data = request.get_json(force=True)
    token = data.get('token') or None
    # allow Authorization: Bearer <token>
    if not token:
        authh = request.headers.get('Authorization', '')
        if authh.lower().startswith('bearer '):
            token = authh.split(None, 1)[1]
    if not token:
        return jsonify({'error': 'missing_token'}), 400
    login.logout(token)
    return jsonify({'ok': True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5646, debug=True)
