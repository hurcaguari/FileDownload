import logging
from urllib import request
from requests import get
from os.path import join, exists, getsize, dirname
from os import makedirs
from math import ceil
from .get import get_property, get_out_path
from .out_cmd import print_cmd

logger = logging.getLogger(__name__)

URL = ''
perty = {}
inx = 0

def dow_list(http_list, path): # 列表参数处理
    global inx
    inx += 1
    path = get_out_path('')['path'] if not path else path
    for i in http_list:
        pathup = dirname(i) if isinstance(i, str) else path
        pathup = pathup.split('/')[-1] if isinstance(i, str) else path
        dow_list(i, path) if isinstance(i, list) else dow_file(i, join(path, pathup))

def dow_file(url, file=''): # 主入口
    global URL, perty
    URL = url
    perty = get_property(url)
    perty['file']['path'] = file if file else perty['file']['path']
    path = join(perty['file']['path'], perty['file']['name'])
    if exists(path):
        if getsize(path) == perty['size']['bytes']:
            print_cmd(perty, 100, Resume=True)
        else:
            resume(perty)
    else:
        if float(perty['size']['KB']) > 128:
            file_load_max(perty)
        else:
            file_load(perty)

def file_load(perty): # 小文件下载函数
    logger.info(f"开始下载小文件: {perty['file']['name']}")
    print_cmd(perty)
    path = join(perty['file']['path'], perty['file']['name'])
    create_directory(perty['file']['path'])
    if perty['status'] == 200:
        request.urlretrieve(perty['url'], path)
    print_cmd(perty, 100)
    logger.info(f"小文件下载完成: {perty['file']['name']}")

def file_load_max(perty): # 大文件下载函数
    logger.info(f"开始下载大文件: {perty['file']['name']}")
    path = join(perty['file']['path'], perty['file']['name'])
    create_directory(perty['file']['path'])
    if perty['status'] == 200:
        request.urlretrieve(perty['url'], path, reporthook=schedule)
    logger.info(f"大文件下载完成: {perty['file']['name']}")

def schedule(blocknum, blocksize, totalsize, Resume=False): # 进度条对接函数
    percent = totalsize / blocksize
    per = 100 / percent
    percent = ceil(blocknum * per)
    percent = 100 if 100 - percent < per else percent
    print_cmd(perty, percent, Resume)

def resume(perty): # 断点续传下载
    logger.info(f"开始断点续传下载: {perty['file']['name']}")
    block = 8192
    path = join(perty['file']['path'], perty['file']['name'])
    temp_size = getsize(path) if exists(path) else 0
    headers = {'Range': 'bytes=%d-' % temp_size}
    r = get(perty['url'], stream=True, verify=False, headers=headers)
    schedule(temp_size / block, block, perty['size']['bytes'], Resume=True)
    with open(path, 'ab') as f:
        for chunk in r.iter_content(chunk_size=block):
            if chunk:
                temp_size += len(chunk)
                f.write(chunk)
                f.flush()
                schedule(temp_size / block, block, perty['size']['bytes'])
    logger.info(f"断点续传下载完成: {perty['file']['name']}")

def create_directory(path):
    if not exists(path):
        makedirs(path)
        logger.info(f"创建目录: {path}")