import logging
from Download import download

# 配置日志记录器
logging.basicConfig(
    level=logging.DEBUG,  # 设置日志级别
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # 设置日志格式
    handlers=[
        logging.FileHandler("app.log"),  # 将日志写入文件
        logging.StreamHandler()  # 将日志输出到控制台
    ]
)

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
    logging.info("开始下载视频文件")
    download(http_list,'C:\\Users\\Hurca\\Downloads\\mov')
    logging.info("视频文件下载完成")

    logging.info("开始下载图片文件")
    download(img_list,'C:\\Users\\Hurca\\Downloads\\img')
    logging.info("图片文件下载完成")