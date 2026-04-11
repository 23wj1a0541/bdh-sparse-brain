from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app) # This lets your frontend talk to the server

# Load the JSON data
with open('activations.json', 'r') as f:
    data = json.load(f)

@app.route('/')
def home():
    return "API is running! Go to /tokens to see available words."

@app.route('/tokens')
def tokens():
    # Return the list of words we have data for
    return jsonify(list(data.keys()))

@app.route('/activate')
def activate():
    token = request.args.get('token', 'currency')
    if token in data:
        # Return real BDH sparse data + simulated dense transformer data
        return jsonify({
            "bdh": data[token],
            "transformer": {"density": [0.95]}, 
            "source": "real"
        })
    return jsonify({"error": "Token not found"}), 404

if __name__ == '__main__':
    app.run(port=5001)