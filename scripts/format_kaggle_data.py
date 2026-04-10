import pandas as pd
import numpy as np
import re
import os

input_path = "data/Amazon_Reviews.csv"
output_path = "data/amazon_reviews_ready.csv"

print(f"Loading raw Kaggle data from {input_path}...")
# Pandas usually chokes on huge unescaped text quotes in Kaggle data, so we use the slower but safer python engine
df = pd.read_csv(input_path, engine='python', on_bad_lines='skip')

# Extract integer from "Rated X out of 5 stars"
def extract_rating(rating_str):
    try:
        return float(re.search(r'\d+', str(rating_str)).group())
    except:
        return 3.0

print("Extracting columns and generating ML Labels...")
df['rating'] = df['Rating'].apply(extract_rating)
df['text'] = df['Review Text'].fillna(df['Review Title']).astype(str)

# The Kaggle dataset does not contain True/False labels or Behavioral metrics.
# For the scope of this project, we must synthesize the labels and identity metrics
# to create a "Weakly Supervised" dataset so the Random Forest model can actually train!
np.random.seed(42)
labels = []
account_ages = []
verified_purchases = []
multiple_ips = []

for idx, row in df.iterrows():
    # Simulate a 15% fake review rate in the real world
    is_fake = np.random.choice([0, 1], p=[0.85, 0.15])
    labels.append(is_fake)
    
    if is_fake == 1:
        # Fakes usually have young accounts, rarely verified, often from flagged IPs
        account_ages.append(np.random.randint(1, 30))
        verified_purchases.append(np.random.choice([0, 1], p=[0.9, 0.1]))
        multiple_ips.append(np.random.choice([1, 0], p=[0.8, 0.2]))
    else:
        # Genuine users have older accounts, usually verified, normal IP behavior
        account_ages.append(np.random.randint(100, 2000))
        verified_purchases.append(np.random.choice([1, 0], p=[0.85, 0.15]))
        multiple_ips.append(0)

df['label'] = labels
df['account_age_days'] = account_ages
df['verified_purchase'] = verified_purchases
df['multiple_ips'] = multiple_ips

# Keep only the columns needed for our Feature Extraction pipeline and Sample 500 rows!
# (Running all 21,058 rows through BERT on a standard laptop CPU will crash due to Out-Of-Memory limits)
final_df = df[['text', 'rating', 'account_age_days', 'verified_purchase', 'multiple_ips', 'label']].sample(n=500, random_state=42)

final_df.to_csv(output_path, index=False)
print(f"✅ Successfully formatted {len(final_df)} Amazon reviews and saved to {output_path}!")
