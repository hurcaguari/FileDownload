from Download import download



http_list = [
    'http://syxiaojuzi.com/video/01.mp4',
    'http://syxiaojuzi.com/video/02.mp4',
    'http://syxiaojuzi.com/video/03.mp4',
    'http://syxiaojuzi.com/video/04.mp4',
    'http://syxiaojuzi.com/video/05.mp4',
    'http://syxiaojuzi.com/video/06.mp4'
]

img_list  =[
    ['http://syxiaojuzi.com/manhua/1/{}.jpg'.format(str(i).zfill(2)) for i in range(1,28)],
    ['http://syxiaojuzi.com/manhua/2/{}.jpg'.format(str(i).zfill(2)) for i in range(1,28)],
    ['http://syxiaojuzi.com/manhua/3/{}.jpg'.format(str(i).zfill(2)) for i in range(1,28)],
    ['http://syxiaojuzi.com/manhua/4/{}.jpg'.format(str(i).zfill(2)) for i in range(1,28)]
]

if __name__ == "__main__":
    download(http_list,'C:\\Users\\Hurca\\Downloads\\mov')
    download(img_list,'C:\\Users\\Hurca\\Downloads\\img')