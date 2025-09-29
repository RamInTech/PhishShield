import pandas as pd
import os

# Paths to datasets

ENRON_PATH = 'phish_shield/src/ML Models/Email_Dataset/enron_spam_data.csv'
CEAS_PATH = 'phish_shield/src/ML Models/Email_Dataset/CEAS_08.csv'
OUTPUT_DIR = 'phish_shield/src/ML Models/Email_Dataset/data'
OUTPUT_PATH = os.path.join(OUTPUT_DIR, 'emails.csv')

# Load CSVs (assume columns: 'text', 'label')
df_enron = pd.read_csv(ENRON_PATH)
df_ceas = pd.read_csv(CEAS_PATH)

# Combine only the two CSVs
combined_df = pd.concat([df_enron, df_ceas], ignore_index=True)


# Select only the relevant columns for training
# Try 'body' or 'Message' as text column, and 'label' as label column
if 'body' in combined_df.columns:
	text_col = 'body'
elif 'Message' in combined_df.columns:
	text_col = 'Message'
else:
	text_col = 'text'  # fallback

if 'label' in combined_df.columns:
	label_col = 'label'
elif 'Spam/Ham' in combined_df.columns:
	label_col = 'Spam/Ham'
else:
	label_col = 'label'  # fallback

df_clean = combined_df[[text_col, label_col]].copy()
df_clean = df_clean.dropna(subset=[text_col, label_col])

# Shuffle
shuffled_df = df_clean.sample(frac=1, random_state=42).reset_index(drop=True)

# Save cleaned dataset
os.makedirs(OUTPUT_DIR, exist_ok=True)
clean_path = os.path.join(OUTPUT_DIR, 'emails_clean.csv')
shuffled_df.to_csv(clean_path, index=False)

print(f"Cleaned and shuffled dataset saved to {clean_path}!")
