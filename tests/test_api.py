import unittest
import json
from app import create_app

class TestAPI(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app('development')
        self.client = self.app.test_client()
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
    
    def test_predict_missing_fields(self):
        """Test prediction with missing fields"""
        response = self.client.post('/api/predict',
                                   json={'temperature_avg': 25})
        self.assertEqual(response.status_code, 400)
    
    def test_statistics_endpoint(self):
        """Test statistics endpoint"""
        response = self.client.get('/api/statistics')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()