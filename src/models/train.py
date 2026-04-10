import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE

def train_models(X, y):
    """
    Trains baseline Logistic Regression and Random Forest models.
    Applies SMOTE if necessary to handle class imbalance.
    """
    print("Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Applying SMOTE...")
    smote = SMOTE(random_state=42)
    X_train_sm, y_train_sm = smote.fit_resample(X_train, y_train)
    
    # Train Logistic Regression
    print("Training Logistic Regression...")
    lr_model = LogisticRegression(max_iter=1000)
    lr_model.fit(X_train_sm, y_train_sm)
    
    # Train Random Forest
    print("Training Random Forest...")
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train_sm, y_train_sm)
    
    # Save models
    import os
    os.makedirs("models", exist_ok=True)
    with open("models/lr_model.pkl", "wb") as f:
        pickle.dump(lr_model, f)
    with open("models/rf_model.pkl", "wb") as f:
        pickle.dump(rf_model, f)
        
    print("Models trained and saved to models/ directory.")
    return lr_model, rf_model, X_test, y_test

if __name__ == "__main__":
    pass # Will be triggered by main pipeline
