import os
from app import create_app
from config.config import Config

app = create_app(os.getenv('FLASK_ENV', 'development'))

if __name__ == '__main__':
    print(f"Starting Agriculture Yield Predictor on {Config.HOST}:{Config.PORT}")
    print(f"Debug mode: {Config.DEBUG}")
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)