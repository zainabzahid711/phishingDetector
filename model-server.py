# model-server.py
import tldextract
from flask import Flask, request, jsonify
from flask_cors import CORS
from joblib import load
import urllib.parse
import re
import numpy as np

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load your trained model
model = load('model-training/model.joblib')

# Copy your feature extraction function from train_model.py
def extract_features(url):
    try:
        parsed = urllib.parse.urlparse(url)
        domain_info = tldextract.extract(url)
        
        features = {
            "url_length": len(url),
            "num_dots": url.count('.'),
            "num_hyphens": url.count('-'),
            "num_underscore": url.count('_'),
            "num_slash": url.count('/'),
            "num_question": url.count('?'),
            "num_equal": url.count('='),
            "num_at": url.count('@'),
            "num_and": url.count('&'),
            "num_exclamation": url.count('!'),
            "num_space": url.count(' '),
            "num_tilde": url.count('~'),
            "num_comma": url.count(','),
            "num_plus": url.count('+'),
            "num_asterisk": url.count('*'),
            "num_hash": url.count('#'),
            "num_dollar": url.count('$'),
            "num_percent": url.count('%'),
            "domain_length": len(domain_info.domain),
            "subdomain_length": len(domain_info.subdomain),
            "subdomain_count": domain_info.subdomain.count('.') + 1 if domain_info.subdomain else 0,
            "is_ip": int(bool(re.match(r'^\d+\.\d+\.\d+\.\d+$', domain_info.domain))),
            "path_length": len(parsed.path),
            "query_length": len(parsed.query),
            "has_https": int(parsed.scheme == 'https'),
            "has_http": int(parsed.scheme == 'http'),
            "has_port": int(parsed.port is not None),
            "has_redirect": int('//' in url[8:]),
            "short_url": int(len(url) < 15),
            "long_url": int(len(url) > 75),
            "sensitive_words": int(bool(re.search(r'secure|account|update|login|signin|verify|bank|paypal', url, re.I))),
            "is_encoded": int('%' in url),
            "random_string": int(bool(re.search(r'[0-9a-f]{8}', url))),
        }
        return features
    except:
        return {
            "url_length": len(url),
            "num_dots": url.count('.'),
            "num_hyphens": 0,
            "num_underscore": 0,
            "num_slash": 0,
            "num_question": 0,
            "num_equal": 0,
            "num_at": 0,
            "num_and": 0,
            "num_exclamation": 0,
            "num_space": 0,
            "num_tilde": 0,
            "num_comma": 0,
            "num_plus": 0,
            "num_asterisk": 0,
            "num_hash": 0,
            "num_dollar": 0,
            "num_percent": 0,
            "domain_length": 0,
            "subdomain_length": 0,
            "subdomain_count": 0,
            "is_ip": 0,
            "path_length": 0,
            "query_length": 0,
            "has_https": 0,
            "has_http": 0,
            "has_port": 0,
            "has_redirect": 0,
            "short_url": 0,
            "long_url": 0,
            "sensitive_words": 0,
            "is_encoded": 0,
            "random_string": 0
        }

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        url = data['url']
        
        # Extract features
        features = extract_features(url)
        if "error" in features:
            return jsonify({"error": features["error"]}), 400
            
        # Convert features to array in correct order
        feature_names = [
    'url_length', 'num_dots', 'num_hyphens', 'num_underscore', 'num_slash',
    'num_question', 'num_equal', 'num_at', 'num_and', 'num_exclamation',
    'num_space', 'num_tilde', 'num_comma', 'num_plus', 'num_asterisk',
    'num_hash', 'num_dollar', 'num_percent', 'domain_length', 'subdomain_length',
    'subdomain_count', 'is_ip', 'path_length', 'query_length', 'has_https',
    'has_http', 'has_port', 'has_redirect', 'short_url', 'long_url',
    'sensitive_words', 'is_encoded', 'random_string'
]
        feature_values = [features[name] for name in feature_names]
        
        # Make prediction
        prediction = model.predict([feature_values])
        proba = model.predict_proba([feature_values])
        
        return jsonify({
            'isPhishing': bool(prediction[0]),
            'confidence': float(np.max(proba)),
            'features': features  # For debugging
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)