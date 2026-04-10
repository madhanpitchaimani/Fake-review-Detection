import torch
from transformers import BertTokenizer, BertModel
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from textblob import TextBlob
import textstat
import re
import pickle
import os

class FeatureExtractor:
    def __init__(self, model_name="bert-base-uncased"):
        print(f"Loading {model_name}...")
        self.tokenizer = BertTokenizer.from_pretrained(model_name)
        self.model = BertModel.from_pretrained(model_name)
        self.scaler = StandardScaler()
        self.feature_names = []

    def get_bert_embeddings(self, texts):
        embeddings = []
        for text in texts:
            inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=128)
            with torch.no_grad():
                outputs = self.model(**inputs)
            cls_embedding = outputs.last_hidden_state[:, 0, :].numpy()
            embeddings.append(cls_embedding)
        return np.vstack(embeddings)

    def extract_paper_features(self, df):
        """
        Extracts the 6 features from the IEEE Integrated Approach paper.
        Returns the raw values (unscaled).
        """
        # 1. Review Length (Word Count)
        df['word_count'] = df['text'].apply(lambda x: len(str(x).split()))
        
        # 2. Review Subjectivity (TextBlob)
        df['subjectivity'] = df['text'].apply(lambda x: TextBlob(str(x)).sentiment.subjectivity)
        
        # 3. Review Readability (Flesch Reading Ease)
        df['readability'] = df['text'].apply(lambda x: textstat.flesch_reading_ease(str(x)))
        
        # 4. Review Extremity (Deviation from neutral rating 3)
        df['extremity'] = df['rating'].apply(lambda x: abs(x - 3))
        
        # 5. Internal Consistency (Sentiment variance across sentences)
        def get_internal_consistency(text):
            sentences = re.split(r'[.!?]+', str(text))
            sentences = [s.strip() for s in sentences if len(s.strip()) > 2]
            if len(sentences) < 2: return 0.0 # Consistent if only one sentence
            sentiments = [TextBlob(s).sentiment.polarity for s in sentences]
            return np.var(sentiments)
        
        df['internal_consistency'] = df['text'].apply(get_internal_consistency)
        
        # 6. External Consistency (Rating Inconsistency vs Product Average)
        if 'product_id' in df.columns and not df.empty and df['product_id'].nunique() > 1:
            prod_means = df.groupby('product_id')['rating'].transform('mean')
            df['rating_inconsistency'] = abs(df['rating'] - prod_means)
        else:
            df['rating_inconsistency'] = abs(df['rating'] - 4.2) # Default assumption
            
        paper_features = df[['word_count', 'subjectivity', 'readability', 'extremity', 'internal_consistency', 'rating_inconsistency']].values
        return paper_features

    def get_fusion_features(self, df, use_paper_features=True, scaler=None):
        """
        Combines textual embeddings from BERT with behavioral and paper-inspired features.
        Returns (normalized_features, raw_ling_features)
        """
        text_features = self.get_bert_embeddings(df["clean_text"].tolist())
        
        behavioral_features = df[["account_age_days", "verified_purchase", "multiple_ips"]].values
        
        all_features = [text_features, behavioral_features]
        
        raw_paper_features = None
        if use_paper_features:
            raw_paper_features = self.extract_paper_features(df)
            all_features.append(raw_paper_features)
            
        fusion_features = np.hstack(all_features)
        
        # Feature Scaling logic
        if scaler:
            normalized_features = scaler.transform(fusion_features)
        else:
            normalized_features = self.scaler.fit_transform(fusion_features)
            
        # Return both for the API to use model input vs UI display
        raw_ling = {
            "review_depth": float(raw_paper_features[0, 0]) if use_paper_features else 0,
            "subjectivity": float(raw_paper_features[0, 1]) if use_paper_features else 0,
            "readability": float(raw_paper_features[0, 2]) if use_paper_features else 0,
            "extremity": float(raw_paper_features[0, 3]) if use_paper_features else 0,
            "internal_consistency": float(raw_paper_features[0, 4]) if use_paper_features else 0,
            "rating_inconsistency": float(raw_paper_features[0, 5]) if use_paper_features else 0
        } if len(df) == 1 else None

        return normalized_features, raw_ling

if __name__ == "__main__":
    pass
