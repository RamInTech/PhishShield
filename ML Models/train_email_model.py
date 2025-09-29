import re
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix, classification_report
from sklearn.preprocessing import LabelEncoder
import joblib


# Preprocessing function for email text (lowercase, remove non-letters)
def preprocess_email(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Enhanced email feature extraction
def extract_email_features(email_text):
    features = []
    features.append(len(email_text))
    features.append(email_text.count('@'))
    features.append(email_text.count('http'))
    features.append(email_text.count('www'))
    features.append(email_text.count('!'))
    features.append(email_text.count('$'))
    features.append(email_text.count('%'))
    features.append(email_text.count('?'))
    features.append(email_text.count('click'))
    features.append(email_text.count('link'))
    features.append(email_text.count('reward'))
    features.append(email_text.count('gift'))
    features.append(email_text.count('card'))
    features.append(email_text.count('claim'))
    features.append(email_text.count('win'))
    features.append(email_text.count('prize'))
    features.append(email_text.count('congratulations'))
    features.append(email_text.count('amazon'))
    features.append(email_text.count('expires'))
    features.append(email_text.count('urgent'))
    features.append(email_text.count('verify'))
    features.append(email_text.count('update'))
    features.append(email_text.count('account'))
    features.append(email_text.count('password'))
    features.append(email_text.count('support'))
    features.append(email_text.count('team'))
    sender_match = re.search(r'from:\s*"?[^"]*"?\s*<([^>]*)>', email_text)
    sender_domain = sender_match.group(1) if sender_match else ''
    features.append(int('amazon' in sender_domain and 'amaz0n' in sender_domain))
    features.append(int('prizes' in sender_domain or 'support' in sender_domain))
    features.append(int('http' in email_text or 'https' in email_text))
    urgency_keywords = ['hurry', 'expires', 'urgent', 'limited', 'now', 'immediately', '24 hours']
    features.append(int(any(kw in email_text for kw in urgency_keywords)))
    return np.array(features)

# Load the preprocessed dataset
print("Loading preprocessed dataset...")
df_emails = pd.read_csv('ML Models/Email_Dataset/data/emails_preprocessed.csv')

# Check for any missing values
print(f"Dataset shape: {df_emails.shape}")
print(f"Missing values:\n{df_emails.isnull().sum()}")

# Remove any rows with missing values
df_emails = df_emails.dropna(subset=['text_clean', 'label'])

# Convert label to integer if needed
df_emails['label'] = df_emails['label'].astype(int)

# Display label distribution
print(f"Label distribution:\n{df_emails['label'].value_counts()}")


# Split data into training and validation sets
X_train_text, X_val_text, y_train, y_val = train_test_split(
    df_emails['text_clean'], df_emails['label'],
    test_size=0.2, stratify=df_emails['label'], random_state=42)

print(f"Training set size: {len(X_train_text)}")
print(f"Validation set size: {len(X_val_text)}")

# Vectorize text with TF-IDF
print("Vectorizing text data...")
vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
X_train_vec = vectorizer.fit_transform(X_train_text)
X_val_vec = vectorizer.transform(X_val_text)

# Extract enhanced features for each email
print("Extracting enhanced features...")
X_train_extra = np.array([extract_email_features(email) for email in X_train_text])
X_val_extra = np.array([extract_email_features(email) for email in X_val_text])

from scipy.sparse import hstack, csr_matrix
X_train = hstack([X_train_vec, csr_matrix(X_train_extra)])
X_val = hstack([X_val_vec, csr_matrix(X_val_extra)])

# Train a Logistic Regression model
print("Training model...")
model = LogisticRegression(class_weight='balanced', max_iter=1000)
model.fit(X_train, y_train)

# Make predictions on validation set
y_pred = model.predict(X_val)

# Evaluation metrics
print("Model Evaluation:")
print("Accuracy:", accuracy_score(y_val, y_pred))
print("Precision:", precision_score(y_val, y_pred))
print("Recall:", recall_score(y_val, y_pred))
print("Classification report:\n", classification_report(y_val, y_pred, target_names=["Ham", "Spam"]))
print("Confusion Matrix:\n", confusion_matrix(y_val, y_pred))

# Export the trained model and vectorizer
print("Saving model and vectorizer...")
joblib.dump(model, 'ML Models/email_classifier_model.pkl')
joblib.dump(vectorizer, 'ML Models/email_tfidf_vectorizer.pkl')

print("Model training completed successfully!")
