import unittest
import json
from app import create_app


class ErrorHandlerTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.app_context.pop()

    def test_marathon_api_404(self):
        rv = self.client.get(
            '/api/v1.0/foobarbaz',
            follow_redirects=True)
        self.assertTrue(rv.status_code == 404)
        data = json.loads(rv.get_data(as_text=True))
        self.assertTrue('api/v1.0/foobarbaz' in data['URI'])

    def test_app_404(self):
        rv = self.client.get(
            '/foobarbaz',
            follow_redirects=True)
        self.assertTrue(rv.status_code == 404)
        self.assertTrue('foobarbaz' in rv.get_data(as_text=True))

