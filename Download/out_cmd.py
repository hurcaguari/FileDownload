import sys,time

'''
进度条绘制类
'''

def print_cmd(perty,rate = 0,Resume = False):
    if len(perty):
        if rate > 0:
            sys.stdout.write(u'\u001b[1A')
        else:
            print('='*110)
            print('下载链接: {}'.format(perty['url']))
            print('文件名称: {} 文件大小: {} KB 状态代码: {}'.format(perty['file']['name'],perty['size']['KB'],perty['status']))
            print('保存位置: {}'.format(perty['file']['path']))

        if Resume:
            print('='*110)
            print('下载链接: {}'.format(perty['url']))
            print('文件名称: {} 文件大小: {} KB 状态代码: {}'.format(perty['file']['name'],perty['size']['KB'],perty['status']))
            print('保存位置: {}'.format(perty['file']['path']))
            Resume = False
        bar = '■'*int(rate)
        bax = '-' * int(100 - rate)
        sys.stdout.write(u'\u001b[1000D\u001b[2K下载进度: '+ bar + bax + '\n')
        sys.stdout.write(u'\u001b[1000D\u001b[2K')
        sys.stdout.flush()