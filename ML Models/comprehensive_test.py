import re
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix, classification_report
import joblib

# Preprocessing function for email text (lowercase, remove non-letters)
def preprocess_email(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Load the trained model and vectorizer
print("Loading trained model and vectorizer...")
model = joblib.load('phish_shield/src/ML Models/email_classifier_model.pkl')
vectorizer = joblib.load('phish_shield/src/ML Models/email_tfidf_vectorizer.pkl')

# Load the preprocessed dataset
print("Loading preprocessed dataset...")
df_emails = pd.read_csv('phish_shield/src/ML Models/Email_Dataset/data/emails_preprocessed.csv')

# Check for any missing values
print(f"Dataset shape: {df_emails.shape}")
print(f"Missing values:\n{df_emails.isnull().sum()}")

# Remove any rows with missing values
df_emails = df_emails.dropna(subset=['text_clean', 'label'])

# Convert label to integer if needed
df_emails['label'] = df_emails['label'].astype(int)

# Display label distribution
print(f"Label distribution:\n{df_emails['label'].value_counts()}")

# Take a random sample of 1000 emails for testing
df_sample = df_emails.sample(n=1000, random_state=42)

# Preprocess the sample emails
df_sample['text_clean'] = df_sample['text_clean'].apply(preprocess_email)

# Vectorize the preprocessed emails
X_test = vectorizer.transform(df_sample['text_clean'])
y_true = df_sample['label']

# Make predictions
y_pred = model.predict(X_test)

# Evaluation metrics
print("\nComprehensive Model Evaluation:")
print("=" * 50)
print("Accuracy:", accuracy_score(y_true, y_pred))
print("Precision:", precision_score(y_true, y_pred))
print("Recall:", recall_score(y_true, y_pred))
print("Classification report:\n", classification_report(y_true, y_pred, target_names=["Ham", "Spam"]))
print("Confusion Matrix:\n", confusion_matrix(y_true, y_pred))

print("\n" + "=" * 50)
print("Comprehensive test completed successfully!")
