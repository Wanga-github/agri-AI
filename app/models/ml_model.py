import joblib
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.model_selection import cross_val_score

class YieldPredictor:
    """Machine Learning model for yield prediction"""
    
    def __init__(self, model_type='random_forest'):
        self.model_type = model_type
        self.model = self._initialize_model()
        self.is_trained = False
    
    def _initialize_model(self):
        """Initialize the ML model"""
        if self.model_type == 'random_forest':
            return RandomForestRegressor(
                n_estimators=200,
                max_depth=15,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42,
                n_jobs=-1
            )
        elif self.model_type == 'gradient_boosting':
            return GradientBoostingRegressor(
                n_estimators=200,
                learning_rate=0.1,
                max_depth=5,
                random_state=42
            )
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")
    
    def train(self, X_train, y_train, X_test=None, y_test=None):
        """Train the model"""
        self.model.fit(X_train, y_train)
        self.is_trained = True
        
        # Evaluate if test data provided
        metrics = {}
        if X_test is not None and y_test is not None:
            metrics = self.evaluate(X_test, y_test)
        
        return metrics
    
    def predict(self, X):
        """Make predictions"""
        if not self.is_trained:
            raise Exception("Model not trained yet!")
        
        predictions = self.model.predict(X)
        return predictions
    
    def evaluate(self, X_test, y_test):
        """Evaluate model performance"""
        predictions = self.predict(X_test)
        
        metrics = {
            'rmse': np.sqrt(mean_squared_error(y_test, predictions)),
            'mae': mean_absolute_error(y_test, predictions),
            'r2_score': r2_score(y_test, predictions),
            'mape': np.mean(np.abs((y_test - predictions) / y_test)) * 100
        }
        
        return metrics
    
    def cross_validate(self, X, y, cv=5):
        """Perform cross-validation"""
        scores = cross_val_score(
            self.model, X, y,
            cv=cv,
            scoring='neg_mean_squared_error'
        )
        rmse_scores = np.sqrt(-scores)
        
        return {
            'cv_rmse_mean': rmse_scores.mean(),
            'cv_rmse_std': rmse_scores.std()
        }
    
    def get_feature_importance(self):
        """Get feature importance"""
        if hasattr(self.model, 'feature_importances_'):
            return self.model.feature_importances_
        return None
    
    def save(self, filepath):
        """Save model to disk"""
        joblib.dump(self.model, filepath)
    
    def load(self, filepath):
        """Load model from disk"""
        self.model = joblib.load(filepath)
        self.is_trained = True