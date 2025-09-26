from flask import Flask, render_template, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hello')
def hello():
    return jsonify({'message': 'Hello from Flask front end!'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
