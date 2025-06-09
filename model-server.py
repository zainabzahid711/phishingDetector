from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from joblib import load
import tldextract
import urllib.parse
import re
import numpy as np
from datetime import datetime
import validators
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={
    r"/predict": {"origins":["chrome-extension://*", "http://localhost:*"]}
})

# Rate Limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)


# Security Headers
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response


# Configuration
TRUSTED_DOMAINS = {
     'amazon.com', 'facebook.com', 'microsoft.com',
    'google.com', 'apple.com', 'aws.amazon.com'
    , 'github.com', 'youtube.com', 'linkedin.com',
    'twitter.com', 'instagram.com', 'reddit.com',
    'pinterest.com', 'wikipedia.org', 'stackoverflow.com',
    'bing.com', 'yahoo.com', 'quora.com', 'tumblr.com',
    'paypal.com', 'dropbox.com', 'slack.com', 'zoom.us',
    'wordpress.com', 'blogger.com', 'medium.com',
    'mailchimp.com', 'bitly.com', 'bitbucket.org',
    'cloudflare.com', 'shopify.com', 'stripe.com',
    'adobe.com', 'salesforce.com', 'oracle.com',
    'microsoftonline.com', 'office.com', 'onedrive.com',
    'live.com', 'outlook.com', 'hotmail.com',
    'icloud.com', 'yandex.ru', 'vk.com', 'alibaba.com',
    'taobao.com', 'weibo.com', 'qq.com', 'baidu.com',
    'tencent.com', 'jd.com', 'sina.com.cn', 'sohu.com',
    '163.com', '126.com', 'aliyun.com', '360.cn',
    'samsung.com', 'huawei.com', 'xiaomi.com',
    'oppo.com', 'vivo.com', 'lenovo.com', 'asus.com',
    'dell.com', 'hp.com', 'acer.com', 'lg.com',
    'sony.com', 'canon.com', 'nikon.com', 'fujifilm.com',
    'adidas.com', 'nike.com', 'puma.com', 'reebok.com',
    'underarmour.com', 'newbalance.com', 'vans.com',
    'converse.com', 'zara.com', 'hm.com', 'uniqlo.com',
    'gap.com', 'oldnavy.com', 'forever21.com',

    'target.com', 'walmart.com', 'costco.com',
    'bestbuy.com', 'ikea.com', 'lowes.com', 'homedepot.com',
    'sears.com', 'macys.com', 'nordstrom.com',
    'ebay.com', 'aliexpress.com', 'etsy.com',
    'craigslist.org', 'craigslist.com', 'olx.com',
    'gumtree.com', 'mercadolibre.com', 'rakuten.com',
    'booking.com', 'airbnb.com', 'expedia.com',
    'tripadvisor.com', 'hotels.com', 'trivago.com',
    'skyscanner.com', 'kayak.com', 'orbitz.com',
    'southwest.com', 'delta.com', 'united.com',
    'americanexpress.com', 'visa.com', 'mastercard.com',
    'discover.com', 'paypal.com', 'squareup.com',
    'stripe.com', 'braintreepayments.com', 'venmo.com',
    'zellepay.com', 'cash.app', 'revolut.com',
    'wise.com', 'transferwise.com', 'remitly.com',
    'westernunion.com', 'moneygram.com', 'worldremit.com',
    'paypal.me', 'paypal.com.au', 'paypal.co.uk',
    'paypal.ca', 'paypal.de', 'paypal.fr',
    'paypal.it', 'paypal.es', 'paypal.nl',
    'paypal.se', 'paypal.no', 'paypal.fi',
    'paypal.dk', 'paypal.pl', 'paypal.ru',
    'paypal.in', 'paypal.co.jp', 'paypal.com.br',
    'paypal.com.mx', 'paypal.com.ar', 'paypal.cl',
    'paypal.com.co', 'paypal.com.pe', 'paypal.com.ve',
    'paypal.com.ec', 'paypal.com.uy', 'paypal.com.py',
    'paypal.com.gt', 'paypal.com.hn', 'paypal.com.sv',
    'paypal.com.ni', 'paypal.com.cr', 'paypal.com.pa',
    'paypal.com.do', 'paypal.com.pr', 'paypal.com.jm',
    'paypal.com.tt', 'paypal.com.bb', 'paypal.com.bs',

    'paypal.com.bz', 'paypal.com.cu', 'paypal.com.hn',

    'paypal.com.gt', 'paypal.com.sv', 'paypal.com.ni',
    'paypal.com.cr', 'paypal.com.pa', 'paypal.com.do',
    'paypal.com.pr', 'paypal.com.jm', 'paypal.com.tt',
    'paypal.com.bb', 'paypal.com.bs', 'paypal.com.bz',
    'paypal.com.cu', 'paypal.com.mx', 'paypal.com.ar',

}

CLOUD_SERVICES = {
    'amazonaws.com', 'cloudfront.net', 
    'azurewebsites.net', 'googleusercontent.com'
    , 'cloudapp.net', 'cloudfunctions.net',
    'cloudflare.com', 'akamaihd.net', 'firebaseapp.com',
    'netlify.app', 'herokuapp.com', 'vercel.app',
    'githubusercontent.com', 'bitbucket.io',
    'gitlab.io', 's3.amazonaws.com', 's3.us-west-1.amazonaws.com',
    's3.us-east-1.amazonaws.com', 's3.eu-west-1.amazonaws.com',
    's3.ap-southeast-1.amazonaws.com', 's3.ap-northeast-1.amazonaws.com',
    's3.sa-east-1.amazonaws.com', 's3.ca-central-1.amazonaws.com',
    's3.eu-central-1.amazonaws.com', 's3.ap-south-1.amazonaws.com',
    's3.us-gov-west-1.amazonaws.com', 's3.us-gov-east-1.amazonaws.com',
    's3.us-west-2.amazonaws.com', 's3.us-west-1.amazonaws.com',
    's3.eu-west-2.amazonaws.com', 's3.eu-west-3.amazonaws.com',
    's3.eu-north-1.amazonaws.com', 's3.ap-southeast-2.amazonaws.com',
    's3.ap-southeast-3.amazonaws.com', 's3.ap-northeast-2.amazonaws.com',
    's3.ap-northeast-3.amazonaws.com', 's3.ca-west-1.amazonaws.com',
    's3.ca-east-1.amazonaws.com', 's3.eu-south-1.amazonaws.com',
    's3.eu-west-4.amazonaws.com', 's3.eu-central-2.amazonaws.com',
    's3.af-south-1.amazonaws.com', 's3.me-south-1.amazonaws.com',
    's3.ap-southeast-4.amazonaws.com', 's3.ap-southeast-5.amazonaws.com',
    's3.ap-southeast-6.amazonaws.com', 's3.ap-southeast-7.amazonaws.com',
    's3.ap-southeast-8.amazonaws.com', 's3.ap-southeast-9.amazonaws.com',
    's3.ap-southeast-10.amazonaws.com', 's3.ap-southeast-11.amazonaws.com',
    's3.ap-southeast-12.amazonaws.com', 's3.ap-southeast-13.amazonaws.com',
    's3.ap-southeast-14.amazonaws.com', 's3.ap-southeast-15.amazonaws.com',
    's3.ap-southeast-16.amazonaws.com', 's3.ap-southeast-17.amazonaws.com',
    's3.ap-southeast-18.amazonaws.com', 's3.ap-southeast-19.amazonaws.com',
    's3.ap-southeast-20.amazonaws.com', 's3.ap-southeast-21.amazonaws.com',
    's3.ap-southeast-22.amazonaws.com', 's3.ap-southeast-23.amazonaws.com',
    's3.ap-southeast-24.amazonaws.com', 's3.ap-southeast-25.amazonaws.com',
    's3.ap-southeast-26.amazonaws.com', 's3.ap-southeast-27.amazonaws.com',
    's3.ap-southeast-28.amazonaws.com', 's3.ap-southeast-29.amazonaws.com',
    's3.ap-southeast-30.amazonaws.com', 's3.ap-southeast-31.amazonaws.com',
    's3.ap-southeast-32.amazonaws.com', 's3.ap-southeast-33.amazonaws.com',
    's3.ap-southeast-34.amazonaws.com', 's3.ap-southeast-35.amazonaws.com',
    's3.ap-southeast-36.amazonaws.com', 's3.ap-southeast-37.amazonaws.com', 
    's3.ap-southeast-38.amazonaws.com', 's3.ap-southeast-39.amazonaws.com',
    's3.ap-southeast-40.amazonaws.com', 's3.ap-southeast-41.amazonaws.com',
    's3.ap-southeast-42.amazonaws.com', 's3.ap-southeast-43.amazonaws.com',
    's3.ap-southeast-44.amazonaws.com', 's3.ap-southeast-45.amazonaws.com',
    's3.ap-southeast-46.amazonaws.com', 's3.ap-southeast-47.amazonaws.com',
    's3.ap-southeast-48.amazonaws.com', 's3.ap-southeast-49.amazonaws.com',
    's3.ap-southeast-50.amazonaws.com', 's3.ap-southeast-51.amazonaws.com',
    's3.ap-southeast-52.amazonaws.com', 's3.ap-southeast-53.amazonaws.com',
    's3.ap-southeast-54.amazonaws.com', 's3.ap-southeast-55.amazonaws.com',
    's3.ap-southeast-56.amazonaws.com', 's3.ap-southeast-57.amazonaws.com',
    's3.ap-southeast-58.amazonaws.com', 's3.ap-southeast-59.amazonaws.com',
    's3.ap-southeast-60.amazonaws.com', 's3.ap-southeast-61.amazonaws.com',
    's3.ap-southeast-62.amazonaws.com', 's3.ap-southeast-63.amazonaws.com',

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
        if not validators.url(url):
            return None
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
    
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    })

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
            'domain': domain,
            'model_version': '1.0.0',
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        print(f"Prediction error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)