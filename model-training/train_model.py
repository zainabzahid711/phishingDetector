import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from joblib import dump
import urllib.parse
import tldextract
import re

# 1. Load dataset
df = pd.read_csv("phishing_site_urls.csv")

# 2. Enhanced feature extraction
def extract_features(url):
    try:
        parsed = urllib.parse.urlparse(url)
        domain_info = tldextract.extract(url)
        
        # Basic URL features
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
            
            # Domain features
            "domain_length": len(domain_info.domain),
            "subdomain_length": len(domain_info.subdomain),
            "subdomain_count": domain_info.subdomain.count('.') + 1 if domain_info.subdomain else 0,
            "is_ip": int(bool(re.match(r'^\d+\.\d+\.\d+\.\d+$', domain_info.domain))),
            
            # Path features
            "path_length": len(parsed.path),
            "query_length": len(parsed.query),
            
            # Security features
            "has_https": int(parsed.scheme == 'https'),
            "has_http": int(parsed.scheme == 'http'),
            "has_port": int(parsed.port is not None),
            
            # Suspicious patterns
            "has_redirect": int('//' in url[8:]),
            "short_url": int(len(url) < 15),
            "long_url": int(len(url) > 75),
            "sensitive_words": int(bool(re.search(r'secure|account|update|login|signin|verify|bank|paypal', url, re.I))),
            "is_encoded": int('%' in url),
            "random_string": int(bool(re.search(r'[0-9a-f]{8}', url))),
        }
        
        return features
    
    except:
        # Return default features if URL parsing fails
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

print("Extracting features...")
df['features'] = df['URL'].apply(extract_features)
X = pd.json_normalize(df['features'])
y = df['Label'].map({'bad': 1, 'good': 0})  # Convert labels to binary

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Train model
print("Training model...")
model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

# 4. Evaluate model
print("Evaluating model...")
y_pred = model.predict(X_test)
print("\nClassification Report:")
print(classification_report(y_test, y_pred))
print("\nAccuracy:", accuracy_score(y_test, y_pred))

# 5. Save model
dump(model, "model.joblib")
print("\nModel trained and saved!")