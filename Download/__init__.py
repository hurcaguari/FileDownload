r"""
单线程自动下载模块:
    - from Download import download
    - download({下载URL或URL列表},{文件保存位置可在Propers中设置})
"""

from Download.get_url import dow_file
from Download.get_url import dow_list

def download(date,path = ''): # 类接口
    dow_list(date,path) if type(date) == list else None
    dow_file(date,path) if type(date) == str else None