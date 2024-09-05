import unittest
from Download.get_url import dow_file, dow_list

class TestDownload(unittest.TestCase):

    def test_dow_file(self):
        # 设置测试数据
        test_data = {
            'file': {'path': 'C:\\Users\\Hurca\\Downloads\\', 'name': 'test_file'},
            'size': {'bytes': 1256, 'KB': '1.23'},
            'status': 404,
            'url': 'http://example.com/test_file'
        }
        
        # 调用函数
        result = dow_file('http://example.com/test_file')
    
        # 断言结果
        self.assertEqual(result, test_data)

    def test_dow_list(self):
        # 设置测试数据
        test_data = [
            {
                'file': {'path': 'C:\\Users\\Hurca\\Downloads\\', 'name': 'test_file1'},
                'size': {'bytes': 1256, 'KB': '1.23'},
                'status': 404,
                'url': 'http://example.com/test_file1'
            },
            {
                'file': {'path': 'C:\\Users\\Hurca\\Downloads\\', 'name': 'test_file2'},
                'size': {'bytes': 1256, 'KB': '1.23'},
                'status': 404,
                'url': 'http://example.com/test_file2'
            }
        ]
        
        urls = ['http://example.com/test_file1', 'http://example.com/test_file2']
        
        # 调用函数
        result = dow_list(urls)
        
        # 断言结果
        self.assertEqual(result, test_data)

if __name__ == '__main__':
    unittest.main()