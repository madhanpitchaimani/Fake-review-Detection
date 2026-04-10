import pandas as pd
import re
from imblearn.over_sampling import SMOTE

def clean_text(text):
    """
    Cleans text by removing special characters, converting to lowercase, etc.
    """
    if pd.isna(text): return ""
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = text.lower().strip()
    return text

def preprocess_data(data_path="data/synthetic_reviews.csv"):
    """
    Loads raw data, cleans text, and balances using SMOTE if necessary.
    """
    print(f"Loading data from {data_path}...")
    df = pd.read_csv(data_path)
    
    print("Cleaning text...")
    df["clean_text"] = df["text"].apply(clean_text)
    
    # Normally SMOTE is applied AFTER feature extraction (on vectors/embeddings), 
    # not on raw text. This will be integrated into the training pipeline.
    
    return df

if __name__ == "__main__":
    df = preprocess_data()
    print(df.head())
