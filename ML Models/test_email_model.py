import re
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
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

# Sample email texts for testing
sample_emails = [
    "Congratulations! You've won $1000 in our lottery. Click here to claim your prize now!",
    "Hi John, can we schedule a meeting for tomorrow at 10am to discuss the project?",
    "URGENT: Your account will be suspended unless you verify your information immediately.",
    "Thanks for the meeting today. I've attached the documents we discussed.",
    "Get rich quick with this amazing investment opportunity! Limited time offer!",
    "Please find the quarterly report attached for your review."
]

# Preprocess the sample emails
preprocessed_emails = [preprocess_email(email) for email in sample_emails]

# Vectorize the preprocessed emails
X_test = vectorizer.transform(preprocessed_emails)

# Make predictions
predictions = model.predict(X_test)
prediction_probabilities = model.predict_proba(X_test)

# Display results
print("\nModel Test Results:")
print("=" * 50)
for i, email in enumerate(sample_emails):
    print(f"\nEmail: {email[:50]}{'...' if len(email) > 50 else ''}")
    print(f"Preprocessed: {preprocessed_emails[i][:50]}{'...' if len(preprocessed_emails[i]) > 50 else ''}")
    print(f"Prediction: {'Spam' if predictions[i] == 1 else 'Ham'}")
    print(f"Confidence: {max(prediction_probabilities[i]):.2%}")

print("\n" + "=" * 50)
print("Test completed successfully!")
