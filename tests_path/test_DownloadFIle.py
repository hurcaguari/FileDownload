import unittest
from Download import DownloadFile

class TestDownloadFile(unittest.TestCase):

    def test_download_file_success(self):
        url = "http://syxiaojuzi.com/video/01.mp4"
        name = "testfile.mp4"
        result = DownloadFile(url, name)
        self.assertIsInstance(result, dict)
        self.assertEqual(result['status'], 200)
        self.assertIn('size', result)
        self.assertIn('path', result)
        self.assertIn('name', result)
        self.assertIn('url', result)

    def test_download_file_not_found(self):
        url = "http://example.com/notfound.mp4"
        name = "notfound.mp4"
        result = DownloadFile(url, name)
        self.assertIsInstance(result, dict)
        self.assertNotEqual(result['status'], 200)

    def test_invalid_url_type(self):
        url = ["http://example.com/testfile.mp4"]
        name = "testfile.mp4"
        result = DownloadFile(url, name)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()