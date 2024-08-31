'''
文件下载类
'''

from urllib import request
from requests import get
from os.path import join
from os.path import exists
from os.path import getsize
from os.path import dirname
from os import makedirs
from math import ceil
from .get import get_property
from .get import get_out_path
from .out_cmd import print_cmd




URL = ''
perty = {}
inx = 0

def dow_list(http_list,path): # 列表参数处理
    global inx
    inx += 1
    path = get_out_path('')['path'] if not path else path
    for i in http_list:
        pathup = dirname(i) if isinstance(i,str) else path
        pathup = pathup.split('/')[-1] if isinstance(i,str) else path
        dow_list(i,path) if isinstance(i,list) else dow_file(i,path+'\\'+ pathup)
        

def dow_file(url,file = ''): # 主入口
    global URL,perty
    URL = url
    perty = get_property(url) 
    perty['file']['path'] = file if file else perty['file']['path']
    path = join(perty['file']['path'],perty['file']['name'])
    if exists(path):
        print_cmd(perty,100,Resume=True) if getsize(path) == perty['size']['bytes'] else resume(perty)
    else:
        file_load(perty) if not float(perty['size']['KB']) > 128 else file_load_max(perty)


def file_load(perty): # 小文件下载函数
    print_cmd(perty)
    path = join(perty['file']['path'],perty['file']['name'])
    makedirs(perty['file']['path']) if not exists(perty['file']['path']) else None
    request.urlretrieve(perty['url'],path) if perty['status'] == 200 else None
    print_cmd(perty,100)

def file_load_max(perty): # 大文件下载函数
    
    path = join(perty['file']['path'],perty['file']['name'])
    makedirs(perty['file']['path']) if not exists(perty['file']['path']) else None
    request.urlretrieve(perty['url'],path,reporthook=schedule) if perty['status'] == 200 else None

def schedule(blocknum,blocksize,totalsize,Resume = False): # 进度条对接函数
    percent = totalsize / blocksize
    per = 100 / percent
    percent = ceil(blocknum * per)
    percent = 100 if 100 - percent < per else percent
    print_cmd(perty,percent,Resume)

def resume(perty): # 断点续传下载
    block = 8192
    path = join(perty['file']['path'],perty['file']['name'])
    temp_size = getsize(path) if exists(path) else 0
    headers = {'Range': 'bytes=%d-' % temp_size}
    r = get(perty['url'],stream=True,verify=False,headers=headers)
    schedule(temp_size/block,block,perty['size']['bytes'],Resume = True)
    with open(path,'ab') as f:
        for chunk in r.iter_content(chunk_size=block):
            if chunk:
                temp_size += len(chunk)
                f.write(chunk)
                f.flush()
                schedule(temp_size/block,block,perty['size']['bytes'])