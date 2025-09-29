
import numpy as np
import pandas as pd
from scipy.sparse import hstack, csr_matrix
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, recall_score
import joblib

# URL lexical feature extraction
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

# Load binary dataset
df_urls = pd.read_csv('ML Models/URL_Dataset/url_dataset_cleaned_shuffled.csv')

# Ensure binary labels (0=safe, 1=phishing)
df_urls = df_urls[df_urls['label'].isin([0,1])]

# Compute lexical feature matrix
lex_feats = np.array([extract_url_features(u) for u in df_urls['url']])

vectorizer_url = TfidfVectorizer(analyzer='char', ngram_range=(3,5), max_features=1000)
X_ngrams = vectorizer_url.fit_transform(df_urls['url'])

X_lex = csr_matrix(lex_feats)
X = hstack([X_ngrams, X_lex])

y = df_urls['label'].values
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)


model_url = LogisticRegression(solver='lbfgs', class_weight='balanced', max_iter=2000)
model_url.fit(X_train, y_train)

from sklearn.metrics import f1_score, precision_recall_curve
y_val_proba = model_url.predict_proba(X_val)
phish_idx_url = list(model_url.classes_).index(1)
phish_proba_val = y_val_proba[:, phish_idx_url]
y_val_phish = (y_val == 1).astype(int)

precisions, recalls, thresholds = precision_recall_curve(y_val_phish, phish_proba_val)
f1s = 2 * (precisions * recalls) / (precisions + recalls + 1e-8)
best_idx = np.argmax(f1s)
best_thresh_url = thresholds[best_idx] if best_idx < len(thresholds) else 0.5
best_f1_url = f1s[best_idx]
print(f"URL classifier phishing threshold (best F1): {best_thresh_url:.2f}, F1: {best_f1_url:.2f}")

y_val_pred = (phish_proba_val >= best_thresh_url).astype(int)
print("URL Classifier Report:\n", classification_report(y_val, y_val_pred, target_names=["Safe", "Phishing"]))
print("Confusion Matrix:\n", confusion_matrix(y_val, y_val_pred))

# Export model and vectorizer
joblib.dump(model_url, 'ML Models/url_classifier_model.pkl')
joblib.dump(vectorizer_url, 'ML Models/url_tfidf_vectorizer.pkl')
