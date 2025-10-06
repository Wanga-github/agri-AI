from flask import Blueprint, request, jsonify
from app.services.prediction_service import PredictionService
from app.services.data_service import DataService

api_bp = Blueprint('api', __name__)

prediction_service = PredictionService()
data_service = DataService()

@api_bp.route('/predict', methods=['POST'])
def predict():
    """API endpoint for yield prediction"""
    try:
        data = request.get_json()
        
        # Validate input
        required_fields = [
            'temperature_avg', 'rainfall_mm', 'humidity_percent',
            'soil_ph', 'soil_nitrogen', 'soil_phosphorus', 'soil_potassium',
            'fertilizer_used_kg', 'irrigation_hours', 'area_hectares'
        ]
        
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Make prediction
        result = prediction_service.predict_yield(data)
        
        return jsonify({
            'success': True,
            'data': result
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/historical', methods=['GET'])
def get_historical():
    """Get historical data"""
    try:
        limit = request.args.get('limit', 100, type=int)
        data = data_service.get_historical_data(limit)
        
        return jsonify({
            'success': True,
            'data': data
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/statistics', methods=['GET'])
def get_statistics():
    """Get data statistics"""
    try:
        stats = data_service.get_statistics()
        
        return jsonify({
            'success': True,
            'data': stats
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Agriculture Yield Predictor API'
    }), 200