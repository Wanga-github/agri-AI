import pandas as pd
import os
from config.config import Config

class DataService:
    """Service for data management"""
    
    def __init__(self):
        self.data_dir = Config.DATA_DIR
    
    def get_historical_data(self, limit=100):
        """Get historical yield data"""
        try:
            filepath = os.path.join(self.data_dir, 'raw', 'sample_data.csv')
            if os.path.exists(filepath):
                df = pd.read_csv(filepath)
                return df.tail(limit).to_dict('records')
            return []
        except Exception as e:
            raise Exception(f"Error fetching historical data: {str(e)}")
    
    def get_statistics(self):
        """Get data statistics"""
        try:
            filepath = os.path.join(self.data_dir, 'raw', 'sample_data.csv')
            if os.path.exists(filepath):
                df = pd.read_csv(filepath)
                
                stats = {
                    'total_records': len(df),
                    'average_yield': round(df['yield_tons_per_hectare'].mean(), 2),
                    'max_yield': round(df['yield_tons_per_hectare'].max(), 2),
                    'min_yield': round(df['yield_tons_per_hectare'].min(), 2),
                    'std_yield': round(df['yield_tons_per_hectare'].std(), 2)
                }
                
                return stats
            return {}
        except Exception as e:
            raise Exception(f"Error calculating statistics: {str(e)}")