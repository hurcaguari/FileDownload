from json import load as JsonLoad
from re import sub as re_sub
from os.path import splitext, basename, normpath as os_normpath
from urllib.parse import urlparse, urlunparse, quote

import urllib.request
import urllib.error

def pro_json(path='.\\Download\\Propers.json'):
    with open(path, 'r') as json:
        return JsonLoad(json)

def sanitize_filename(filename):
    # 移除文件名中的无效字符
    return re_sub(r'[<>:"/\\|?*]', '_', filename)

def get_out_path(url):
    # 获取文件保存路径
    return os_normpath(pro_json()['PATH'])

def get_file_extension(url):
    # 从URL中提取文件扩展名
    return splitext(basename(url))[1]

def remove_url_params(url):
    # 剔除URL中的请求参数
    parsed_url = urlparse(url)
    return urlunparse(parsed_url._replace(query='', fragment=''))

def encode_url(url):
    # 对URL进行编码
    parsed_url = urlparse(url)
    encoded_path = quote(parsed_url.path)
    url = urlunparse(parsed_url._replace(path=encoded_path))
    return url

def get_property(url, name):
    url = remove_url_params(url)
    url = encode_url(url)
    out_dict = {
        'name': splitext(basename(name))[0],
        'url': url,
        'status': None,
        'size': None,
        'path': {
            'path': get_out_path(url),
            'file': splitext(basename(sanitize_filename(name)))[0],
            'extension': get_file_extension(url)
        }
    }
    try:
        res = urllib.request.urlopen(url)
    except urllib.error.HTTPError as error:
        out_dict['status'] = error
        return out_dict
    except urllib.error.URLError as error:
        out_dict['status'] = error
        return out_dict
    out_dict['size'] = int(res.headers['Content-Length'])
    out_dict['status'] = res.code
    return out_dict