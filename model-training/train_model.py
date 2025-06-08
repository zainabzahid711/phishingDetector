import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from joblib import dump
import urllib.parse
import tldextract
import re
import os

def load_data():
    """Load and clean the training data"""
    try:
        main_df = pd.read_csv("phishing_site_urls.csv")
        aug_df = pd.read_csv("augmented_urls.csv")
        df = pd.concat([main_df, aug_df])
        
        # Clean data
        df = df.drop_duplicates(subset=['URL'])
        df = df[df['URL'].notna()]
        df = df[df['Label'].notna()]
        df = df[df['URL'].apply(lambda x: isinstance(x, str))]
        df = df[df['URL'].apply(lambda x: urllib.parse.urlparse(x).scheme in ['http','https'])]
        
        return df
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        raise

def extract_features(url):
    """Extract features from URL - only the features we'll use in the model"""
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
    except Exception as e:
        print(f"Error extracting features: {str(e)}")
        return None

def train_model():
    """Train and save the model"""
    try:
        df = load_data()
        print(f"Loaded {len(df)} samples")
        
        # Extract features
        df['features'] = df['URL'].apply(extract_features)
        df = df[df['features'].notna()]

        if len(df) == 0:
            raise ValueError("No valid URLs after feature extraction.")
        
        X = pd.json_normalize(df['features'])
        y = df['Label'].map({'bad': 1, 'good': 0})

        if y.isna().any():
            print("Warning: Some labels are missing. Samples:")
            print(df[y.isna()]['URL'])
            y = y.fillna(0)
            
        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Train model
        model = GradientBoostingClassifier(
            n_estimators=200,
            learning_rate=0.05,
            max_depth=5,
            validation_fraction=0.2,
            n_iter_no_change=10,
            random_state=42
        )
        model.fit(X_train, y_train)
        
        # Evaluate
        print("\nClassification Report:")
        print(classification_report(y_test, model.predict(X_test)))
        print("\nConfusion Matrix:")
        print(confusion_matrix(y_test, model.predict(X_test)))
        
        # Save model with feature names
        os.makedirs("model-training", exist_ok=True)
        dump((model, X.columns.tolist()), "model-training/model.joblib")
        print("\nModel trained and saved successfully!")
        
        return model
    except Exception as e:
        print(f"Training error: {str(e)}")
        raise

if __name__ == '__main__':
    train_model()