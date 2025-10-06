import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    
    # Paths
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    MODEL_PATH = os.getenv('MODEL_PATH', os.path.join(DATA_DIR, 'models', 'yield_predictor.pkl'))
    SCALER_PATH = os.getenv('SCALER_PATH', os.path.join(DATA_DIR, 'models', 'scaler.pkl'))
    
    # Model parameters
    RANDOM_STATE = 42
    TEST_SIZE = 0.2
    
class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}