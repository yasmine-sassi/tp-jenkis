import unittest
from unittest.mock import patch, MagicMock
from app import app

class TestApp(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    @patch('app.cache')
    def test_index(self, mock_cache):
        mock_cache.incr.return_value = 5
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'5', response.data)

    def test_health(self):
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'OK')

if __name__ == '__main__':
    unittest.main()