import sys

'''
进度条绘制类
'''

def print_titen(perty):
    print('='*110)
    print('下载链接: {}'.format(perty['url']))
    print('文件名称: {} 文件大小: {:.2f} KB 状态代码: {}'.format(perty['path']['file'],int(perty['size'])/1024,perty['status']))
    print('保存位置: {}'.format(perty['path']['path']))

def print_error(perty):
    print('='*110)
    print('下载链接: {}'.format(perty['url']))
    print('文件名称: {} 文件大小: {} KB 状态代码: {}'.format(perty['path']['file'],perty['size'],perty['status']))
    print('保存位置: {}'.format(perty['path']['path']))

def progress_bar(perty, rate=0, Resume=False):
    """
    打印命令行输出。\n

    参数：\n
    >perty (dict): 包含下载信息的字典。\n
    >rate (int, optional): 下载进度百分比。默认为0。\n
    >Resume (bool, optional): 是否继续下载。默认为False。\n
    """
    if len(perty):
        if rate > 0:
            sys.stdout.write(u'\u001b[1A')
        else:
            print_titen(perty) if perty['status'] == 200 else print_error(perty)
        if Resume:
            print_titen(perty) if perty['status'] == 200 else print_error(perty)
            Resume = False

        Resume = False
        bar = '■'*int(rate)
        bax = '-' * int(100 - rate)
        sys.stdout.write(u'\u001b[1000D\u001b[2K下载进度: '+ bar + bax + '\n')
        sys.stdout.write(u'\u001b[1000D\u001b[2K')
        sys.stdout.flush()