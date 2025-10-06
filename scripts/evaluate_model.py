import os
import sys
import joblib
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.ml_model import YieldPredictor
from app.models.data_processor import DataProcessor
from config.config import Config

def evaluate_model():
    """Evaluate the trained model"""
    print("Loading model and data...")
    
    # Initialize
    processor = DataProcessor()
    model = YieldPredictor()
    
    # Load model and scaler
    model.load(Config.MODEL_PATH)
    processor.scaler = joblib.load(Config.SCALER_PATH)
    
    # Load data
    data_path = os.path.join(Config.DATA_DIR, 'raw', 'sample_data.csv')
    df = processor.load_data(data_path)
    
    # Preprocess
    X, y = processor.preprocess(df, fit=False)
    
    # Split
    X_train, X_test, y_train, y_test = processor.split_data(X, y)
    
    # Predictions
    y_pred = model.predict(X_test)
    
    # Evaluate
    metrics = model.evaluate(X_test, y_test)
    
    print("\n" + "="*50)
    print("MODEL EVALUATION")
    print("="*50)
    for metric, value in metrics.items():
        print(f"{metric.upper()}: {value:.4f}")
    
    # Visualizations
    print("\nGenerating visualizations...")
    
    # 1. Actual vs Predicted
    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, y_pred, alpha=0.5)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
    plt.xlabel('Actual Yield (tons/hectare)')
    plt.ylabel('Predicted Yield (tons/hectare)')
    plt.title('Actual vs Predicted Yield')
    plt.tight_layout()
    plt.savefig('evaluation_actual_vs_predicted.png')
    print("Saved: evaluation_actual_vs_predicted.png")
    
    # 2. Residuals
    residuals = y_test - y_pred
    plt.figure(figsize=(10, 6))
    plt.scatter(y_pred, residuals, alpha=0.5)
    plt.axhline(y=0, color='r', linestyle='--')
    plt.xlabel('Predicted Yield (tons/hectare)')
    plt.ylabel('Residuals')
    plt.title('Residual Plot')
    plt.tight_layout()
    plt.savefig('evaluation_residuals.png')
    print("Saved: evaluation_residuals.png")
    
    # 3. Distribution of residuals
    plt.figure(figsize=(10, 6))
    sns.histplot(residuals, kde=True)
    plt.xlabel('Residuals')
    plt.ylabel('Frequency')
    plt.title('Distribution of Residuals')
    plt.tight_layout()
    plt.savefig('evaluation_residuals_dist.png')
    print("Saved: evaluation_residuals_dist.png")
    
    print("\nEvaluation complete!")

if __name__ == '__main__':
    evaluate_model()