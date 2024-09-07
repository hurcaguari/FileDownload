r"""
单线程自动下载模块:
    - from Download import download
    - download({下载URL或URL列表},{文件保存位置可在Propers中设置})
"""

from Download.FileDownload import dow_file


def DownloadFile(url:str,name:str, path = '') -> dict:
    """
    根据给定的URL下载文件并将其保存到指定的文件路径。\n
    参数：\n
    >date (str): 要下载的文件的URL。\n
    >name (str): 要下载的文件的名称。\n
    >path (str, 可选): 文件下载的路径。默认为空字符串。\n
    返回：\n
    >(dict, None): 下载的文件的属性或参数错误则为None。\n
    """
    return dow_file(url,name, path) if type(url) == str else None