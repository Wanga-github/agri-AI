import os
import joblib
from app.models.ml_model import YieldPredictor
from app.models.data_processor import DataProcessor
from config.config import Config

class PredictionService:
    """Service for making predictions"""
    
    def __init__(self):
        self.model = YieldPredictor()
        self.processor = DataProcessor()
        self._load_models()
    
    def _load_models(self):
        """Load trained models"""
        try:
            if os.path.exists(Config.MODEL_PATH):
                self.model.load(Config.MODEL_PATH)
                print(f"Model loaded from {Config.MODEL_PATH}")
            
            if os.path.exists(Config.SCALER_PATH):
                self.processor.scaler = joblib.load(Config.SCALER_PATH)
                print(f"Scaler loaded from {Config.SCALER_PATH}")
        except Exception as e:
            print(f"Warning: Could not load models: {str(e)}")
    
    def predict_yield(self, input_data):
        """Predict crop yield"""
        try:
            # Prepare input
            X_scaled = self.processor.prepare_input(input_data)
            
            # Make prediction
            prediction = self.model.predict(X_scaled)[0]
            
            # Calculate confidence interval (simple approach)
            confidence = self._calculate_confidence(prediction)
            
            return {
                'predicted_yield': round(float(prediction), 2),
                'unit': 'tons per hectare',
                'confidence_interval': {
                    'lower': round(float(prediction * 0.9), 2),
                    'upper': round(float(prediction * 1.1), 2)
                },
                'confidence_score': confidence,
                'recommendations': self._generate_recommendations(input_data, prediction)
            }
        except Exception as e:
            raise Exception(f"Prediction error: {str(e)}")
    
    def _calculate_confidence(self, prediction):
        """Calculate confidence score (0-100)"""
        # Simplified confidence calculation
        # In production, use prediction intervals from the model
        base_confidence = 75
        variability_factor = min(abs(prediction) / 10, 10)
        confidence = base_confidence + variability_factor
        return min(round(confidence, 2), 95)
    
    def _generate_recommendations(self, input_data, predicted_yield):
        """Generate recommendations based on input and prediction"""
        recommendations = []
        
        # Rainfall recommendations
        if input_data['rainfall_mm'] < 500:
            recommendations.append({
                'type': 'irrigation',
                'priority': 'high',
                'message': 'Low rainfall detected. Increase irrigation to maintain optimal soil moisture.'
            })
        
        # Soil nutrient recommendations
        npk_total = (input_data['soil_nitrogen'] + 
                    input_data['soil_phosphorus'] + 
                    input_data['soil_potassium'])
        
        if npk_total < 50:
            recommendations.append({
                'type': 'fertilizer',
                'priority': 'high',
                'message': 'Soil nutrient levels are low. Consider applying balanced NPK fertilizer.'
            })
        
        # Soil pH recommendations
        if input_data['soil_ph'] < 6.0 or input_data['soil_ph'] > 7.5:
            recommendations.append({
                'type': 'soil_management',
                'priority': 'medium',
                'message': f'Soil pH ({input_data["soil_ph"]}) is outside optimal range (6.0-7.5). Consider soil amendment.'
            })
        
        # Yield optimization
        if predicted_yield < 3.0:
            recommendations.append({
                'type': 'yield_optimization',
                'priority': 'medium',
                'message': 'Predicted yield is below average. Review crop management practices and consider soil testing.'
            })
        
        return recommendations