import unittest
from app import app
import json

class URLShortenerTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_create_short_url(self):
        response = self.app.post('/api/url', json={"original_url": "https://example.com"})
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn("short_url", data)
        self.assertEqual(data["original_url"], "https://example.com")

    def test_get_all_urls(self):
        response = self.app.get('/api/url')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)

    def test_get_specific_url(self):
        # First, create a new short URL
        post_resp = self.app.post('/api/url', json={"original_url": "https://getone.com"})
        short_url = post_resp.get_json()["short_url"]
        # Now, get it
        get_resp = self.app.get(f'/api/url/{short_url}')
        self.assertEqual(get_resp.status_code, 200)
        data = get_resp.get_json()
        self.assertEqual(data["original_url"], "https://getone.com")

    def test_delete_url(self):
        # Create a new short URL
        post_resp = self.app.post('/api/url', json={"original_url": "https://delete.com"})
        short_url = post_resp.get_json()["short_url"]
        # Delete it
        del_resp = self.app.delete(f'/api/url/{short_url}')
        self.assertEqual(del_resp.status_code, 204)
        # Try to get it again
        get_resp = self.app.get(f'/api/url/{short_url}')
        self.assertEqual(get_resp.status_code, 404)

    def test_create_url_missing_field(self):
        response = self.app.post('/api/url', json={})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("error", data)

    def test_get_nonexistent_url(self):
        response = self.app.get('/api/url/nonexistent')
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertIn("error", data)

    def test_delete_nonexistent_url(self):
        response = self.app.delete('/api/url/nonexistent')
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertIn("error", data)

if __name__ == '__main__':
    unittest.main() 