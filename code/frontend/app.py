from flask import Flask, jsonify, Response
from flask_cors import CORS
import os
import subprocess
import mimetypes

app = Flask(__name__)
CORS(app)

# Get the build directory path
BUILD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'build')

def get_mime_type(filename):
    """Get MIME type for a file"""
    mime_type, _ = mimetypes.guess_type(filename)
    return mime_type or 'application/octet-stream'

def read_file_content(filepath):
    """Read file content using subprocess to avoid Docker filesystem lock issues"""
    try:
        # Use cat command to bypass Python's file locking issues in Docker
        result = subprocess.run(['cat', filepath], capture_output=True, timeout=5)
        if result.returncode == 0:
            return result.stdout
        return None
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        return None

# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    # Handle static files
    if path != "":
        file_path = os.path.join(BUILD_DIR, path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            content = read_file_content(file_path)
            if content is not None:
                return Response(content, mimetype=get_mime_type(file_path))
    
    # Serve index.html for root and any unmatched routes (SPA routing)
    index_path = os.path.join(BUILD_DIR, 'index.html')
    content = read_file_content(index_path)
    if content is not None:
        return Response(content, mimetype='text/html')
    
    return "Build not found. Please run 'npm run build' first.", 404

# API routes
@app.route('/api/hello')
def hello():
    version = 'unknown'
    try:
        result = subprocess.run(['cat', os.path.join(os.path.dirname(__file__), 'VERSION')], 
                               capture_output=True, timeout=5)
        if result.returncode == 0:
            version = result.stdout.decode('utf-8').strip()
    except Exception:
        pass
    return jsonify({'message': 'Hello from Flask front end!', 'version': version})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False, threaded=True)
