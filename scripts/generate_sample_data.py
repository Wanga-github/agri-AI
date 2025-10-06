import pandas as pd
import numpy as np
import os

def generate_sample_data(n_samples=1000):
    """Generate sample agricultural data"""
    np.random.seed(42)
    
    data = {
        'temperature_avg': np.random.uniform(15, 35, n_samples),
        'rainfall_mm': np.random.uniform(300, 1500, n_samples),
        'humidity_percent': np.random.uniform(40, 90, n_samples),
        'soil_ph': np.random.uniform(5.5, 8.0, n_samples),
        'soil_nitrogen': np.random.uniform(10, 40, n_samples),
        'soil_phosphorus': np.random.uniform(5, 30, n_samples),
        'soil_potassium': np.random.uniform(10, 35, n_samples),
        'fertilizer_used_kg': np.random.uniform(50, 200, n_samples),
        'irrigation_hours': np.random.uniform(100, 400, n_samples),
        'area_hectares': np.random.uniform(1, 20, n_samples)
    }
    
    df = pd.DataFrame(data)
    
    # Generate yield based on features (with some realistic correlations)
    df['yield_tons_per_hectare'] = (
        0.05 * df['temperature_avg'] +
        0.002 * df['rainfall_mm'] +
        0.01 * df['humidity_percent'] +
        0.3 * df['soil_ph'] +
        0.08 * df['soil_nitrogen'] +
        0.06 * df['soil_phosphorus'] +
        0.05 * df['soil_potassium'] +
        0.01 * df['fertilizer_used_kg'] +
        0.005 * df['irrigation_hours'] +
        np.random.normal(0, 0.5, n_samples)  # Add noise
    )
    
    # Ensure positive yields
    df['yield_tons_per_hectare'] = df['yield_tons_per_hectare'].clip(lower=0.5)
    
    return df

if __name__ == '__main__':
    # Create directories if they don't exist
    os.makedirs('data/raw', exist_ok=True)
    
    # Generate and save data
    df = generate_sample_data(1000)
    output_path = 'data/raw/sample_data.csv'
    df.to_csv(output_path, index=False)
    
    print(f"Sample data generated and saved to {output_path}")
    print(f"Shape: {df.shape}")
    print("\nFirst few rows:")
    print(df.head())
    print("\nBasic statistics:")
    print(df.describe())