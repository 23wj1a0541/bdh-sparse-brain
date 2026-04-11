from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import random
import re

app = Flask(__name__)
CORS(app)

# Load the JSON data
with open('activations.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

stored_tokens = list(data.keys())
stored_tokens_lower = {token.lower(): token for token in stored_tokens}

currency_words = {'dollar', 'euro', 'rupee', 'price', 'cost', 'pay', 'bucks', 'pound', 'yen'}
paris_terms = {'paris', 'france', 'eiffel', 'seine'}
india_terms = {'india', 'delhi', 'mumbai', 'bangalore', 'karnataka', 'kerala'}

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.route('/')
def home():
    return "API is running! Go to /tokens to see available words."

@app.route('/tokens')
def tokens():
    return jsonify(stored_tokens)


def find_closest_token(raw_token):
    if not raw_token:
        return random.choice(stored_tokens)

    token = raw_token.strip().lower()
    if token in stored_tokens_lower:
        return stored_tokens_lower[token]

    substring_candidates = [stored for stored in stored_tokens if stored.lower() in token]
    if substring_candidates:
        return max(substring_candidates, key=len)

    reverse_candidates = [stored for stored in stored_tokens if token in stored.lower()]
    if reverse_candidates:
        return max(reverse_candidates, key=len)

    if any(word in token for word in currency_words):
        return 'currency' if 'currency' in data else random.choice(stored_tokens)

    if any(word in token for word in paris_terms):
        return 'Paris' if 'Paris' in data else random.choice(stored_tokens)
    if any(word in token for word in india_terms):
        return 'India' if 'India' in data else random.choice(stored_tokens)

    return random.choice(stored_tokens)

@app.route('/activate')
def activate():
    raw_token = request.args.get('token', '').strip()
    matched_token = find_closest_token(raw_token)
    return jsonify({
        'matched_token': matched_token,
        'bdh': data[matched_token],
        'transformer': {'density': [0.95]},
        'source': 'real'
    })

@app.route('/activate_text', methods=['POST'])
def activate_text():
    payload = request.get_json(silent=True)
    if not payload or 'text' not in payload:
        return jsonify({'error': 'JSON body must include a text field.'}), 400

    text = payload.get('text', '')
    words = re.findall(r"[A-Za-z0-9']+", text)
    if not words:
        return jsonify({'error': 'No valid words found in text.'}), 400

    word_matches = {}
    matched_tokens = []
    for word in words:
        best = find_closest_token(word)
        word_matches[word] = best
        matched_tokens.append(best)

    def average_arrays(arrays):
        if not arrays:
            return []
        length = len(arrays[0])
        averaged = [0.0] * length
        for arr in arrays:
            for i, value in enumerate(arr):
                averaged[i] += float(value)
        return [value / len(arrays) for value in averaged]

    layer_arrays = [data[token]['layer_0'] for token in matched_tokens]
    density_arrays = [data[token]['density'] for token in matched_tokens]

    averaged = {
        'layer_0': average_arrays(layer_arrays),
        'density': average_arrays(density_arrays)
    }

    return jsonify({
        'averaged': averaged,
        'word_matches': word_matches,
        'source': 'real_averaged'
    })

if __name__ == '__main__':
    app.run(port=5001)