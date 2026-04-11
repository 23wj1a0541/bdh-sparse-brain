from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import random
import re

app = Flask(__name__)
CORS(app)

# Load the JSON data
with open('bdh/activations.json', 'r', encoding='utf-8') as f:
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


def build_sigma_snapshot(layer_0):
    first32 = layer_0[:32] if len(layer_0) >= 32 else layer_0 + [0.0] * (32 - len(layer_0))
    # Threshold to top 5% active
    if first32:
        sorted_vals = sorted(first32, reverse=True)
        threshold = sorted_vals[min(len(sorted_vals) - 1, int(len(first32) * 0.05))]
        first32 = [v if v >= threshold else 0.0 for v in first32]
    raw_values = []
    for i in range(32):
        for j in range(32):
            if i == j:
                raw_values.append(0.0)
            else:
                value = first32[i] * first32[j]
                value = value * value
                value += random.uniform(0, 0.05)
                raw_values.append(value)

    non_diag = [v for v in raw_values if v > 0]
    if not non_diag:
        return raw_values

    sorted_values = sorted(non_diag)
    threshold_index = max(0, int(len(sorted_values) * 0.9) - 1)
    threshold = sorted_values[threshold_index]
    max_value = sorted_values[-1]
    min_value = sorted_values[0]

    scaled_snapshot = []
    for idx, value in enumerate(raw_values):
        if value == 0.0:
            scaled_snapshot.append(0.0)
            continue

        if value <= threshold:
            fade = threshold if threshold > 0 else 1.0
            scaled_snapshot.append(((value / fade) ** 2) * 0.35)
        else:
            bright_range = max_value - threshold if max_value > threshold else threshold
            scaled_snapshot.append(0.35 + 0.65 * ((value - threshold) / bright_range))

    return scaled_snapshot

@app.route('/activate')
def activate():
    raw_token = request.args.get('token', '').strip()
    matched_token = find_closest_token(raw_token)
    return jsonify({
        'matched_token': matched_token,
        'bdh': data[matched_token],
        'transformer': {'density': [0.95]},
        'sigma_snapshot': build_sigma_snapshot(data[matched_token]['layer_0']),
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