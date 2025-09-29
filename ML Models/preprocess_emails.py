import pandas as pd
import re
import os

# Paths
INPUT_PATH = 'phish_shield/src/ML Models/Email_Dataset/data/emails.csv'
OUTPUT_PATH = 'phish_shield/src/ML Models/Email_Dataset/data/emails_preprocessed.csv'

# Preprocessing function for email text
def preprocess_email(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Load dataset
if os.path.exists(INPUT_PATH):
    df = pd.read_csv(INPUT_PATH)
else:
    raise FileNotFoundError(f"Input file not found: {INPUT_PATH}")

# Select columns
if 'body' in df.columns:
    text_col = 'body'
elif 'Message' in df.columns:
    text_col = 'Message'
else:
    text_col = 'text'

if 'label' in df.columns:
    label_col = 'label'
elif 'Spam/Ham' in df.columns:
    label_col = 'Spam/Ham'
else:
    label_col = 'label'

# Drop rows with missing text or label
df_clean = df[[text_col, label_col]].dropna(subset=[text_col, label_col])

# Apply preprocessing
df_clean['text_clean'] = df_clean[text_col].apply(preprocess_email)

# Save cleaned dataset
df_clean[['text_clean', label_col]].to_csv(OUTPUT_PATH, index=False)

print(f"Preprocessed dataset saved as {OUTPUT_PATH}")
