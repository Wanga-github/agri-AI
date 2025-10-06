import os
import sys
import joblib
import pandas as pd

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.ml_model import YieldPredictor
from app.models.data_processor import DataProcessor
from config.config import Config

def train_model():
    """Train the yield prediction model"""
    print("Starting model training...")
    
    # Initialize
    processor = DataProcessor()
    model = YieldPredictor(model_type='random_forest')
    
    # Load data
    data_path = os.path.join(Config.DATA_DIR, 'raw', 'sample_data.csv')
    print(f"Loading data from {data_path}")
    df = processor.load_data(data_path)
    print(f"Loaded {len(df)} records")
    
    # Preprocess
    print("Preprocessing data...")
    X, y = processor.preprocess(df, fit=True)
    
    # Split data
    X_train, X_test, y_train, y_test = processor.split_data(X, y)
    print(f"Training set: {len(X_train)} samples")
    print(f"Test set: {len(X_test)} samples")
    
    # Train model
    print("Training model...")
    metrics = model.train(X_train, y_train, X_test, y_test)
    
    # Print metrics
    print("\n" + "="*50)
    print("MODEL PERFORMANCE METRICS")
    print("="*50)
    for metric, value in metrics.items():
        print(f"{metric.upper()}: {value:.4f}")
    
    # Cross-validation
    print("\nPerforming cross-validation...")
    cv_metrics = model.cross_validate(X_train, y_train)
    print(f"CV RMSE Mean: {cv_metrics['cv_rmse_mean']:.4f} (+/- {cv_metrics['cv_rmse_std']:.4f})")
    
    # Feature importance
    feature_importance = model.get_feature_importance()
    if feature_importance is not None:
        print("\nFeature Importance:")
        feature_names = processor.feature_columns
        importance_df = pd.DataFrame({
            'feature': feature_names,
            'importance': feature_importance
        }).sort_values('importance', ascending=False)
        print(importance_df)
    
    # Save model and scaler
    os.makedirs(os.path.join(Config.DATA_DIR, 'models'), exist_ok=True)
    
    model_path = Config.MODEL_PATH
    scaler_path = Config.SCALER_PATH
    
    model.save(model_path)
    joblib.dump(processor.scaler, scaler_path)
    
    print(f"\nModel saved to {model_path}")
    print(f"Scaler saved to {scaler_path}")
    print("\nTraining complete!")

if __name__ == '__main__':
    train_model()