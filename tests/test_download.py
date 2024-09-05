import unittest
from unittest.mock import patch, MagicMock
from Download.get_url import dow_file, file_load, file_load_max, resume, create_directory
import os

class TestDownload(unittest.TestCase):

    @patch('Download.get_url.get_property')
    @patch('Download.get_url.exists')
    @patch('Download.get_url.getsize')
    @patch('Download.get_url.print_cmd')
    def test_dow_file(self, mock_print_cmd, mock_getsize, mock_exists, mock_get_property):
        mock_get_property.return_value = {
            'file': {'path': 'test_path', 'name': 'test_file'},
            'size': {'bytes': 1024, 'KB': 1},
            'status': 200,
            'url': 'http://example.com/test_file'
        }
        mock_exists.return_value = False
        dow_file('http://example.com/test_file')
        mock_print_cmd.assert_called_with(mock_get_property.return_value, 100)

    @patch('Download.get_url.request.urlretrieve')
    @patch('Download.get_url.create_directory')
    @patch('Download.get_url.print_cmd')
    def test_file_load(self, mock_print_cmd, mock_create_directory, mock_urlretrieve):
        perty = {
            'file': {'path': 'test_path', 'name': 'test_file'},
            'size': {'bytes': 1024, 'KB': 1},
            'status': 200,
            'url': 'http://example.com/test_file'
        }
        file_load(perty)
        mock_create_directory.assert_called_with('test_path')
        mock_urlretrieve.assert_called_with('http://example.com/test_file', os.path.join('test_path', 'test_file'))
        mock_print_cmd.assert_called_with(perty, 100)

    @patch('Download.get_url.request.urlretrieve')
    @patch('Download.get_url.create_directory')
    @patch('Download.get_url.print_cmd')
    def test_file_load_max(self, mock_print_cmd, mock_create_directory, mock_urlretrieve):
        perty = {
            'file': {'path': 'test_path', 'name': 'test_file'},
            'size': {'bytes': 1024 * 1024, 'KB': 1024},
            'status': 200,
            'url': 'http://example.com/test_file'
        }
        file_load_max(perty)
        mock_create_directory.assert_called_with('test_path')
        mock_urlretrieve.assert_called_with('http://example.com/test_file', os.path.join('test_path', 'test_file'), reporthook=unittest.mock.ANY)

    @patch('Download.get_url.get')
    @patch('Download.get_url.getsize')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_resume(self, mock_open, mock_getsize, mock_get):
        mock_getsize.return_value = 512
        mock_response = MagicMock()
        mock_response.iter_content.return_value = [b'chunk1', b'chunk2']
        mock_get.return_value = mock_response
        perty = {
            'file': {'path': 'test_path', 'name': 'test_file'},
            'size': {'bytes': 1024, 'KB': 1},
            'status': 200,
            'url': 'http://example.com/test_file'
        }
        resume(perty)
        mock_open.assert_called_with(os.path.join('test_path', 'test_file'), 'ab')
        mock_get.assert_called_with('http://example.com/test_file', stream=True, verify=False, headers={'Range': 'bytes=512-'})

    def test_create_directory(self):
        with patch('Download.get_url.makedirs') as mock_makedirs:
            create_directory('test_path')
            mock_makedirs.assert_called_with('test_path')

if __name__ == '__main__':
    unittest.main()