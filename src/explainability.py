import shap
import lime
import lime.lime_tabular
import numpy as np

class ExplainabilityModule:
    def __init__(self, model, X_train, feature_names=None):
        print("Initializing Explainability Module...")
        self.model = model
        self.X_train = X_train
        self.feature_names = feature_names
        
    def generate_shap_values(self, X_instance):
        """
        Explain predictions using SHAP.
        Works well with Tree-based models like Random Forest.
        """
        try:
            # Random Forest usually works best with TreeExplainer or simply Explainer
            explainer = shap.Explainer(self.model, self.X_train)
            shap_values = explainer(X_instance)
            return shap_values
        except Exception as e:
            print(f"SHAP Explainer Error: {e}")
            return None

    def generate_lime_explanation(self, X_instance):
        """
        Explain tabular behavioral predictions using LIME.
        Useful for highlighting local feature importance for a single review.
        """
        if self.feature_names is None:
            feature_names = [f"f_{i}" for i in range(self.X_train.shape[1])]
        else:
            feature_names = self.feature_names

        explainer = lime.lime_tabular.LimeTabularExplainer(
            self.X_train, 
            feature_names=feature_names, 
            class_names=['Genuine', 'Fake'], 
            verbose=False, 
            mode='classification'
        )
        
        # Explain the first instance in the batch
        instance = X_instance[0] if len(X_instance.shape) > 1 else X_instance
        exp = explainer.explain_instance(instance, self.model.predict_proba, num_features=10)
        return exp.as_list()

    def get_feature_importance_summary(self):
        """
        Returns the top features that distinguish fake vs credible reviews 
        according to the Random Forest model.
        """
        if not hasattr(self.model, 'feature_importances_'):
            return "Model does not support feature importance."
            
        importances = self.model.feature_importances_
        indices = np.argsort(importances)[::-1]
        
        summary = []
        for i in range(min(10, len(importances))):
            name = self.feature_names[indices[i]] if self.feature_names else f"Feature {indices[i]}"
            summary.append((name, importances[indices[i]]))
            
        return summary
