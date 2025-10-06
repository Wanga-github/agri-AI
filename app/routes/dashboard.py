from flask import Blueprint, render_template, request, jsonify
from app.services.prediction_service import PredictionService
from app.services.data_service import DataService

dashboard_bp = Blueprint('dashboard', __name__)

prediction_service = PredictionService()
data_service = DataService()

@dashboard_bp.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@dashboard_bp.route('/dashboard')
def dashboard():
    """Dashboard page"""
    try:
        stats = data_service.get_statistics()
        return render_template('dashboard.html', stats=stats)
    except:
        return render_template('dashboard.html', stats={})

@dashboard_bp.route('/predict', methods=['GET', 'POST'])
def predict_page():
    """Prediction page"""
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            
            # Convert to float
            for key in data:
                data[key] = float(data[key])
            
            result = prediction_service.predict_yield(data)
            return render_template('prediction.html', result=result, input_data=data)
        
        except Exception as e:
            return render_template('prediction.html', error=str(e))
    
    return render_template('prediction.html')