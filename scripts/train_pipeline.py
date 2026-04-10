import os
import sys
import pandas as pd

# Add root directory to python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.generate_synthetic_data import generate_synthetic_reviews
from src.data_preprocessing import preprocess_data
from src.feature_extraction import FeatureExtractor
from src.models.train import train_models
from src.evaluation import evaluate_model

def main():
    print("--- Starting Fake Review Detection Training Pipeline ---")
    
    # 1. Generate/Load Data
    data_path = "data/synthetic_reviews.csv"
    print(f"Generating synthetic data with 500 samples for better comparison...")
    generate_synthetic_reviews(num_samples=500, output_path=data_path)
    
    # 2. Preprocess Data
    df = preprocess_data(data_path)
    labels = df["label"].values
    
    # 3. COMPARISON: Baseline vs Integrated
    extractor = FeatureExtractor()
    
    print("\n[PHASE 1] Training BASELINE Model (BERT + Behavior Only)...")
    features_base, _ = extractor.get_fusion_features(df, use_paper_features=False)
    _, rf_base, X_test_base, y_test_base = train_models(features_base, labels)
    
    print("\n[PHASE 2] Training INTEGRATED Model (BERT + Behavior + 6 Paper Features)...")
    features_int, _ = extractor.get_fusion_features(df, use_paper_features=True)
    _, rf_int, X_test_int, y_test_int = train_models(features_int, labels)
    
    # 5. Evaluate and Compare
    print("\n" + "="*50)
    print("FINAL COMPARISON RESULTS")
    print("="*50)
    
    print("\n--- Baseline Model (Before Integrated Approach) ---")
    stats_base = evaluate_model(rf_base, X_test_base, y_test_base, model_name="Baseline RF")
    
    print("\n--- Integrated Model (After IEEE Paper Approach) ---")
    stats_int = evaluate_model(rf_int, X_test_int, y_test_int, model_name="Integrated RF")
    
    # 6. Save History for UI Dashboard
    import json
    history = {
        "baseline": stats_base,
        "integrated": stats_int,
        "improvement": {
            "accuracy": stats_int["accuracy"] - stats_base["accuracy"],
            "auc": stats_int["auc"] - stats_base["auc"]
        },
        "features_added": [
            "Review Length",
            "Review Subjectivity",
            "Review Readability",
            "Review Extremity",
            "Internal Consistency",
            "External Consistency"
        ],
        "training_date": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    os.makedirs("models", exist_ok=True)
    with open("models/training_history.json", "w") as f:
        json.dump(history, f, indent=4)
    
    import pickle
    with open("models/rf_model.pkl", "wb") as f:
        pickle.dump(rf_int, f)
        
    # Save the scaler for inference consistency!
    with open("models/scaler.pkl", "wb") as f:
        pickle.dump(extractor.scaler, f)
        
    print("\n✅ Comparison Complete! History saved to `models/training_history.json`.")
    print("New improved model saved as `models/rf_model.pkl`.")
    print("Inference scaler saved as `models/scaler.pkl`.")

if __name__ == "__main__":
    main()
