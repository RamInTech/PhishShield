import joblib
import pandas as pd
import numpy as np
from scipy.sparse import hstack, csr_matrix

def extract_url_features(url):
    suspicious_keywords = [
        'login', 'secure', 'verify', 'account', 'update', 'free', 'paypal', 'bank', 'iphone', 'signin', 'password', 'ebay', 'amazon', 'admin', 'confirm', 'webscr', 'redirect', 'submit', 'id', 'user', 'client', 'auth', 'pay', 'refund', 'win', 'bonus', 'prize', 'alert', 'urgent', 'limited', 'risk', 'protection', 'safe', 'device', 'remove', 'register', 'reset', 'unlock', 'activate', 'support', 'help', 'service', 'access', 'direct', 'deposit', 'royalbank', 'rbc', 'halifax', 'lloyds', 'interac', 'apple', 'google', 'microsoft', 'outlook', 'office', 'mail', 'email', 'sms', 'whatsapp', 'facebook', 'instagram', 'twitter', 'linkedin', 'cloud', 'azure', 'aws', 'netlify', 'xyz', 'online', 'digital', 'site', 'web', 'host', 'domain', 'ssl', 'cert', 'whois', 'registrar', 'phish', 'scam', 'fraud', 'fake', 'malicious', 'danger', 'threat', 'attack', 'hack', 'steal', 'harvest', 'spoof', 'phishing'
    ]
    keyword_features = [int(kw in url.lower()) for kw in suspicious_keywords]
    return [
        len(url),
        sum(c.isdigit() for c in url),
        sum(not c.isalnum() for c in url),
        url.count('.'),
        int('@' in url),
        url.count('-'),
        len(url.split('/')[2]) if url.startswith('http') and len(url.split('/')) > 2 else 0,  # domain length
        int(url.startswith('https')),  # uses HTTPS
    ] + keyword_features

# Load test dataset
print("Loading test dataset...")
df = pd.read_csv('URL_Dataset/url_dataset_cleaned_shuffled.csv')

# Prepare features
lex_feats = np.array([extract_url_features(u) for u in df['url']])
vectorizer = joblib.load('url_tfidf_vectorizer.pkl')
X_ngrams = vectorizer.transform(df['url'])
X_lex = csr_matrix(lex_feats)
X = hstack([X_ngrams, X_lex])

# Load model
model = joblib.load('url_classifier_model.pkl')

# Predict
print("Predicting...")
y_pred = model.predict(X)

# Show results
print(pd.Series(y_pred).value_counts())
print('Sample predictions:', y_pred[:10])
print('True labels:', df['label'][:10].values)
