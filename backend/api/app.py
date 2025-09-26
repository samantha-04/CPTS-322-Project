from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/health')
def hello():
    return jsonify({'status': 200, 'message': 'API is live'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5646, debug=True)
