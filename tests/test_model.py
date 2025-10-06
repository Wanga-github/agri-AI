import unittest
import numpy as np
from app.models.ml_model import YieldPredictor
from app.models.data_processor import DataProcessor

class TestYieldPredictor(unittest.TestCase):
    
    def setUp(self):
        self.model = YieldPredictor()
        self.processor = DataProcessor()
    
    def test_model_initialization(self):
        """Test model initialization"""
        self.assertIsNotNone(self.model.model)
        self.assertFalse(self.model.is_trained)
    
    def test_data_processor(self):
        """Test data processor"""
        # Create sample data
        X = np.random.rand(100, 10)
        
        self.assertEqual(X.shape[0], 100)
        self.assertEqual(X.shape[1], 10)
    
    def test_prediction_shape(self):
        """Test prediction output shape"""
        # Create dummy data
        X_train = np.random.rand(100, 12)
        y_train = np.random.rand(100)
        
        # Train
        self.model.train(X_train, y_train)
        
        # Predict
        X_test = np.random.rand(10, 12)
        predictions = self.model.predict(X_test)
        
        self.assertEqual(len(predictions), 10)

if __name__ == '__main__':
    unittest.main()