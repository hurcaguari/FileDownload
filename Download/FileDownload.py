from urllib import request
from requests import get
from os.path import join, getsize, dirname, normpath

import os
from os import makedirs
from math import ceil
from .Progress import progress_bar
from .Property import get_property

URL = ''
perty = {}
inx = 0


def dow_file(url:str, name:str, path='',) -> dict: # 主入口
    global URL, perty
    URL = url
    perty = get_property(url,name)
    if perty['status'] != 200:
        progress_bar(perty)
        return perty
    file = join(perty['path']['path'], perty['path']['file']+perty['path']['extension'])
    if os.path.exists(file):
        if getsize(file) == perty['size']:
            progress_bar(perty, 100, Resume=True)
        else:
            perty = resume(perty)
        return perty
    else:
        return file_load_max(perty)

def file_load_max(perty:dict) -> dict: # 大文件下载函数
    path = join(perty['path']['path'], perty['path']['file']+perty['path']['extension'])
    create_directory(perty['path']['path'])
    if perty['status'] == 200:
        request.urlretrieve(perty['url'], path, reporthook=schedule)
        return perty
    else:
        return perty

def schedule(blocknum, blocksize, totalsize, Resume=False): # 进度条对接函数
    percent = totalsize / int(blocksize)
    per = 100 / percent
    percent = ceil(blocknum * per)
    percent = 100 if 100 - percent < per else percent
    progress_bar(perty, percent, Resume)

def resume(perty): # 断点续传下载
    block = 8192
    path = join(perty['path']['path'], perty['path']['file']+perty['path']['extension'])
    temp_size = getsize(path) if os.path.exists(path) else 0
    if temp_size == perty['size']:
        progress_bar(perty, 100, Resume=True)
        return perty
    headers = {'Range': 'bytes=%d-' % temp_size}
    try:
        r = get(perty['url'], stream=True, verify=False, headers=headers)
    except Exception as e:
        return perty
    schedule(temp_size / block, block, perty['size'], Resume=True)
    with open(path, 'ab') as f:
        for chunk in r.iter_content(chunk_size=block):
            if chunk:
                temp_size += len(chunk)
                f.write(chunk)
                f.flush()
                schedule(temp_size / block, block, perty['size'])
    return perty

def create_directory(path): # 创建目录
    normalized_path = normpath(path)
    if not os.path.exists(normalized_path):
        makedirs(normalized_path)