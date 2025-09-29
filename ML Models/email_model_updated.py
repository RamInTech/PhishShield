import re
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
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

# Apply preprocessing
df_emails['text_clean'] = df_emails['text_clean'].apply(preprocess_email)

# Split data
X_train_text, X_val_text, y_train, y_val = train_test_split(
    df_emails['text_clean'], df_emails['label'],
    test_size=0.2, stratify=df_emails['label'], random_state=42)

# Vectorize text with TF-IDF
vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
X_train = vectorizer.fit_transform(X_train_text)
X_val = vectorizer.transform(X_val_text)

# Train a Logistic Regression model
class_weights = {0:1, 1:1} # Equal weights for binary classification
model = LogisticRegression(class_weight=class_weights, max_iter=1000)
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
joblib.dump(model, 'phish_shield/src/ML Models/email_classifier_model.pkl')
joblib.dump(vectorizer, 'phish_shield/src/ML Models/email_tfidf_vectorizer.pkl')

print("Model training completed successfully!")


# python "phish_shield/src/ML Models/email_model_updated.py"