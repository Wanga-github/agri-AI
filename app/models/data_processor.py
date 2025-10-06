import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

class DataProcessor:
    """Handle data preprocessing and feature engineering"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.feature_columns = [
            'temperature_avg', 'rainfall_mm', 'humidity_percent',
            'soil_ph', 'soil_nitrogen', 'soil_phosphorus', 'soil_potassium',
            'fertilizer_used_kg', 'irrigation_hours', 'area_hectares'
        ]
    
    def load_data(self, filepath):
        """Load data from CSV file"""
        try:
            df = pd.read_csv(filepath)
            return df
        except Exception as e:
            raise Exception(f"Error loading data: {str(e)}")
    
    def preprocess(self, df, fit=True):
        """Preprocess the data"""
        # Handle missing values
        df = df.fillna(df.mean())
        
        # Feature engineering
        df['temp_rainfall_interaction'] = df['temperature_avg'] * df['rainfall_mm']
        df['npk_total'] = df['soil_nitrogen'] + df['soil_phosphorus'] + df['soil_potassium']
        
        # Update feature columns
        self.feature_columns.extend(['temp_rainfall_interaction', 'npk_total'])
        
        X = df[self.feature_columns]
        
        if fit:
            X_scaled = self.scaler.fit_transform(X)
        else:
            X_scaled = self.scaler.transform(X)
        
        return X_scaled, df['yield_tons_per_hectare'] if 'yield_tons_per_hectare' in df.columns else None
    
    def prepare_input(self, input_data):
        """Prepare input data for prediction"""
        df = pd.DataFrame([input_data])
        
        # Feature engineering
        df['temp_rainfall_interaction'] = df['temperature_avg'] * df['rainfall_mm']
        df['npk_total'] = df['soil_nitrogen'] + df['soil_phosphorus'] + df['soil_potassium']
        
        X = df[self.feature_columns]
        X_scaled = self.scaler.transform(X)
        
        return X_scaled
    
    def split_data(self, X, y, test_size=0.2, random_state=42):
        """Split data into train and test sets"""
        return train_test_split(X, y, test_size=test_size, random_state=random_state)