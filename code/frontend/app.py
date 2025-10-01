from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='build/static')
CORS(app)

# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join('build', path)):
        return send_from_directory('build', path)
    else:
        return send_from_directory('build', 'index.html')

# API routes
@app.route('/api/hello')
def hello():
    return jsonify({'message': 'Hello from Flask front end!'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
