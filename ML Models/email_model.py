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
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Example: Load and combine email datasets (SpamAssassin, Enron, Nazario)
# into a DataFrame
# (Assume `df_emails` has columns ['text', 'label'], where label in {0,1,2})
# df_spam = pd.read_csv('spam_emails.csv'); df_spam['label']=1
# df_ham = pd.read_csv('ham_emails.csv'); df_ham['label']=0
# df_phish= pd.read_csv('phishing_emails.csv'); df_phish['label']=2
# df_emails = pd.concat([df_ham, df_spam, df_phish], ignore_index=True)

# For illustration, assume df_emails is already loaded:
df_emails = pd.DataFrame({
    'text': ["Hello, meeting at 10am", "You have won $1000, click here!", "Verify your account now"],
    'label': [0, 1, 2] # 0=Ham, 1=Spam, 2=Phishing
})

# Apply preprocessing
df_emails['text_clean'] = df_emails['text'].apply(preprocess_email)

# Split data
X_train_text, X_val_text, y_train, y_val = train_test_split(
    df_emails['text_clean'], df_emails['label'],
    test_size=0.2, stratify=df_emails['label'], random_state=42)

# Vectorize text with TF-IDF
vectorizer = TfidfVectorizer(max_features=5000)
X_train = vectorizer.fit_transform(X_train_text)
X_val = vectorizer.transform(X_val_text)

# Train a Logistic Regression (with class weights to emphasize Phishing)
class_weights = {0:1, 1:1, 2:5} # e.g., give phishing 5x weight
model = LogisticRegression(multi_class='multinomial', solver='lbfgs',
                           class_weight=class_weights, max_iter=1000)
model.fit(X_train, y_train)

# Alternatively, one could use an XGBoost multi-class classifier:
# from xgboost import XGBClassifier
# model = XGBClassifier(objective='multi:softprob', num_class=3, random_state=42)
# model.fit(X_train, y_train)

# Compute predicted probabilities on validation data
y_val_proba = model.predict_proba(X_val)

# Identify index of Phishing class (label 2)
phish_idx = list(model.classes_).index(2)
phish_proba = y_val_proba[:, phish_idx]
# True binary labels: 1 if actual phishing, else 0
y_val_phish = (y_val == 2).astype(int)

best_thresh = 0.5
best_recall = 0.0
# Scan thresholds from 0 to 1
for thresh in np.linspace(0, 1, 101):
    # Classify as phishing if probability >= thresh
    y_pred_phish = (phish_proba >= thresh).astype(int)
    recall = recall_score(y_val_phish, y_pred_phish) # recall for phishing
    if recall > best_recall:
        best_recall = recall
        best_thresh = thresh

print(f"Selected phishing threshold: {best_thresh:.2f} with recall {best_recall:.2f}")

# Final predictions on test set (or new data)
X_test = X_val # for demo, use validation as test
y_test = y_val
y_test_proba = model.predict_proba(X_test)
phish_proba_test = y_test_proba[:, phish_idx]
y_pred_base = model.predict(X_test)

# Override with threshold: if P(phishing) >= best_thresh, predict class 2
y_pred = []
for base_pred, ph_proba in zip(y_pred_base, phish_proba_test):
    if ph_proba >= best_thresh:
        y_pred.append(2)
    else:
        y_pred.append(base_pred)
y_pred = np.array(y_pred)

# Evaluation metrics
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification report:\n", classification_report(y_test, y_pred,
                                                      target_names=["Ham","Spam","Phishing"]))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

# Export the trained model and vectorizer
joblib.dump(model, 'email_classifier_model.pkl')
joblib.dump(vectorizer, 'email_tfidf_vectorizer.pkl')
