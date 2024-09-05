import unittest
from unittest.mock import patch
from main import download

class TestDownload(unittest.TestCase):
    @patch('logging.info')
    def test_download_videos(self, mock_logging_info):
        http_list = [
            'http://syxiaojuzi.com/video/01.mp4',
            'http://syxiaojuzi.com/video/02.mp4',
            'http://syxiaojuzi.com/video/03.mp4',
            'http://syxiaojuzi.com/video/04.mp4',
            'http://syxiaojuzi.com/video/05.mp4',
            'http://syxiaojuzi.com/video/06.mp4'
        ]
        download(http_list, 'C:\\Users\\Hurca\\Downloads\\mov')
        mock_logging_info.assert_called_with("视频文件下载完成")

    @patch('logging.info')
    def test_download_images(self, mock_logging_info):
        img_list = [
            ['http://syxiaojuzi.com/manhua/1/{}.jpg'.format(str(i).zfill(2)) for i in range(1, 28)],
            ['http://syxiaojuzi.com/manhua/2/{}.jpg'.format(str(i).zfill(2)) for i in range(1, 28)],
            ['http://syxiaojuzi.com/manhua/3/{}.jpg'.format(str(i).zfill(2)) for i in range(1, 28)],
            ['http://syxiaojuzi.com/manhua/4/{}.jpg'.format(str(i).zfill(2)) for i in range(1, 28)]
        ]
        download(img_list, 'C:\\Users\\Hurca\\Downloads\\img')
        mock_logging_info.assert_called_with("图片文件下载完成")

if __name__ == "__main__":
    unittest.main()