import logging
from urllib import request
from requests import get
from os.path import join, getsize, dirname, normpath
import os
from os import makedirs
from math import ceil
from .get import get_property, get_out_path
from .out_cmd import print_cmd

logger = logging.getLogger(__name__)

URL = ''
perty = {}
inx = 0

def dow_list(http_list: list, path = None): # 列表参数处理
    """
    从给定的HTTP URL列表下载文件。

    参数:
        http_list (list): HTTP URL列表。
        path: 文件下载的路径。

    返回:
        None
    """
    global inx
    inx += 1
    out_list = []
    path = get_out_path('')['path'] if not path else path

    logger.info(f"开始下载列表: {inx}")
    for i in http_list:
        try:
            pathup = dirname(i) if isinstance(i, str) else path
            pathup = pathup.split('/')[-1] if isinstance(i, str) else path
            if isinstance(i, list):
                out_list.append(dow_list(i, join(path, pathup)))
            else:
                out_list.append(dow_file(i, join(path, pathup)))
            logger.info(f"列表下载完成: {inx}")
        except Exception as e:
            logger.error(f"下载失败: {inx}")
            logger.error(e)
    return out_list


def dow_file(url, path=''): # 主入口
    global URL, perty
    URL = url
    perty = get_property(url)
    # perty['file']['path'] = path if path else perty['file']['path']
    file = join(perty['file']['path'], perty['file']['name'])
    if os.path.exists(file):
        if getsize(file) == perty['size']['bytes']:
            print_cmd(perty, 100, Resume=True)
        else:
            return resume(perty)
    else:
        if float(perty['size']['KB']) > 128:
            return file_load_max(perty)
        else:
            return file_load(perty)

def file_load(perty): # 小文件下载函数
    logger.info(f"开始下载小文件: {perty['file']['name']}")
    print_cmd(perty)
    path = join(perty['file']['path'], perty['file']['name'])
    create_directory(perty['file']['path'])
    if perty['status'] == 200:
        try:
            request.urlretrieve(perty['url'], path)
            logger.info(f"小文件下载完成: {perty['file']['name']}")
            print_cmd(perty, 100)
            return perty
        except Exception as e:
            logger.error(f"下载失败: {perty['file']['name']}")
            logger.error(e)
            return perty
    else:
        logger.error(f"下载失败: {perty['file']['name']}")
        return perty

def file_load_max(perty): # 大文件下载函数
    logger.info(f"开始下载大文件: {perty['file']['name']}")
    path = join(perty['file']['path'], perty['file']['name'])
    create_directory(perty['file']['path'])
    if perty['status'] == 200:
        request.urlretrieve(perty['url'], path, reporthook=schedule)
        logger.info(f"大文件下载完成: {perty['file']['name']}")
        return perty
    else:
        logger.error(f"下载失败: {perty['file']['name']}")
        return perty
    

def schedule(blocknum, blocksize, totalsize, Resume=False): # 进度条对接函数
    percent = totalsize / blocksize
    per = 100 / percent
    percent = ceil(blocknum * per)
    percent = 100 if 100 - percent < per else percent
    print_cmd(perty, percent, Resume)

def resume(perty): # 断点续传下载
    logger.info(f"开始断点续传下载: {perty['file']['name']}") # 断点续传下载
    block = 8192
    path = join(perty['file']['path'], perty['file']['name'])
    temp_size = getsize(path) if os.path.exists(path) else 0
    if temp_size == perty['size']['bytes']:
        print_cmd(perty, 100, Resume=True)
        return perty
    headers = {'Range': 'bytes=%d-' % temp_size}
    try:
        r = get(perty['url'], stream=True, verify=False, headers=headers)
    except Exception as e:
        logger.error(f"下载失败: {perty['file']['name']}")
        logger.error(e)
        return perty
    schedule(temp_size / block, block, perty['size']['bytes'], Resume=True)
    with open(path, 'ab') as f:
        for chunk in r.iter_content(chunk_size=block):
            if chunk:
                temp_size += len(chunk)
                f.write(chunk)
                f.flush()
                schedule(temp_size / block, block, perty['size']['bytes'])
    logger.info(f"断点续传下载完成: {perty['file']['name']}")
    return perty

def create_directory(path): # 创建目录
    normalized_path = normpath(path)
    if not os.path.exists(normalized_path):
        makedirs(normalized_path)
        logger.info(f"创建目录: {normalized_path}") 