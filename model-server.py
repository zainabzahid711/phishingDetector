from flask import Flask, request, jsonify
from flask_cors import CORS
from joblib import load
import tldextract
import urllib.parse
import re
import numpy as np

app = Flask(__name__)
CORS(app)

# Configuration
TRUSTED_DOMAINS = {
    'google.com', 'github.com', 'microsoft.com',
}

CLOUD_SERVICES = {
    'amazonaws.com', 'cloudfront.net', 
    'azurewebsites.net', 'googleusercontent.com'
}

ALL_SAFE_DOMAINS = TRUSTED_DOMAINS.union(CLOUD_SERVICES)

MODEL_PATH = "model-training/model.joblib"

# Define the feature names in the exact order the model expects
FEATURE_NAMES = [
    'url_length', 'num_dots', 'num_hyphens', 'num_underscore', 'num_slash',
    'num_question', 'num_equal', 'num_at', 'num_and', 'num_exclamation',
    'num_space', 'num_tilde', 'num_comma', 'num_plus', 'num_asterisk',
    'num_hash', 'num_dollar', 'num_percent', 'domain_length', 'subdomain_length',
    'subdomain_count', 'is_ip', 'path_length', 'query_length', 'has_https',
    'has_http', 'has_port', 'has_redirect', 'short_url', 'long_url',
    'sensitive_words', 'is_encoded', 'random_string'
]

# Load model with proper error handling
try:
    loaded_data = load(MODEL_PATH)
    if isinstance(loaded_data, tuple) and len(loaded_data) == 2:
        model, model_feature_names = loaded_data
        print(f"Model loaded with {len(model_feature_names)} features")
    else:
        model = loaded_data
        print("Model loaded (legacy format), using default feature names")
except Exception as e:
    print(f"Error loading model: {str(e)}")
    raise

def extract_features(url):
    """Extract features from URL - only the features the model expects"""
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
        
        # Return features in the correct order
        return [features[name] for name in FEATURE_NAMES]
    except Exception as e:
        print(f"Feature extraction error: {str(e)}")
        return None

@app.route('/predict', methods=['POST'])
def predict():
    """Handle prediction requests"""
    try:
        # Validate input
        if not request.json or 'url' not in request.json:
            return jsonify({"error": "Missing URL in request"}), 400
        
        url = request.json['url'].strip()
        if not url.startswith(('http://', 'https://')):
            return jsonify({"error": "URL must start with http:// or https://"}), 400
        
        # Check trusted domains
        domain = tldextract.extract(url).domain + '.' + tldextract.extract(url).suffix
        if domain in ALL_SAFE_DOMAINS:
            return jsonify({
                'isPhishing': False,
                'confidence': 0.01 if domain in TRUSTED_DOMAINS else 0.1,
                'message': 'Trusted domain' if domain in TRUSTED_DOMAINS else 'Cloud service'
            })
        
        # Extract features
        features = extract_features(url)
        if features is None:
            return jsonify({"error": "Feature extraction failed"}), 400
        
        # Predict
        prediction = model.predict([features])[0]
        proba = model.predict_proba([features])[0][1]
        
        return jsonify({
            'isPhishing': bool(prediction),
            'confidence': float(proba),
            'domain': domain
        })
        
    except Exception as e:
        print(f"Prediction error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)