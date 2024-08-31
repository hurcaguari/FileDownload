import urllib.request
import urllib.error
from json import load as JsonLoad
from os.path import split

'''
属性获取类
'''

def Propers(path='.\\Download\\Propers.json'):
    with open(path,'r') as json:
        return JsonLoad(json)

def get_size(res):
    fb = int(res)
    fk = "%.2f"%(fb/1024)
    return {"bytes":fb,"KB":fk}

def get_out_path(url):
    path = Propers()['PATH']
    (file_path,filename) = split(url)
    return {'path':path,'name':filename}

def get_property(url):
    try:
        res = urllib.request.urlopen(url)
    except urllib.error.HTTPError as error:
        res = error
    return {'url':url,'status':res.code,'size':get_size(res.headers['Content-Length']),'file':get_out_path(url)}
