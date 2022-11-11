import os
import time
import requests
from threading import Thread

from .config import Config
from .tools import get_header, get_proxy

class Downloader:
    def __init__(self, onDownload):
        # 绑定回调函数
        self.onDownload = onDownload

        # 创建 session
        self.session = requests.session()
        
        # 初始化下载状态
        self.total_size = 0

    def add_url(self, info: dict):
        # 加入下载队列
        # 文件路径
        path = os.path.join(Config.download_path, info["file_name"])

        # 获取总大小
        file_size = self.get_total_size(info["url"], info["referer_url"], path)
        self.total_size += file_size

        # 计算分片下载片段大小，加入线程池
        for chunk_list in self.calc_chunk(file_size, Config.max_thread):
            # 生成下载信息
            url, referer_url = info["url"], info["referer_url"]

            Thread(target = self.range_download, args = (url, referer_url, path, chunk_list, )).start()

    def start_download(self, info: list):
        # 开始下载
        # 初始化下载信息
        self.complete_size, self._flag, self.task = 0, True, []

        # 将 url 加入下载队列
        for value in info:
            self.add_url(value)

        self.onListen()

    def range_download(self, url: str, referer_url: str, path: str, chunk_list: list):
        # 下载分片
        req = self.session.get(url, headers = get_header(referer_url, None, chunk_list), stream = True, proxies = get_proxy())
        
        with open(path, "rb+") as f:
            # 指定写入位置
            f.seek(chunk_list[0])

            # 流式下载
            for chunk in req.iter_content(chunk_size = 32 * 1024):
                # 写入字节流
                if chunk:
                    f.write(chunk)
                    f.flush()

                    self.complete_size += len(chunk)

    def onListen(self):
        # 监听事件
        while True:
            temp_size = self.complete_size

            time.sleep(1)
            
            # 计算速度
            speed = self.format_speed((self.complete_size - temp_size) / 1024)
            
            # 计算进度
            progress = int(self.complete_size / self.total_size * 100)
            
            self.onDownload(progress, speed)

            if progress >= 100:
                break 

    def get_total_size(self, url: str, referer_url: str, path: str) -> int:
        # 获取文件总大小
        request = self.session.head(url, headers = get_header(referer_url))

        total_size = int(request.headers["Content-Length"])
        
        # 本地创建文件
        with open(path, "wb") as f:
            f.truncate(total_size)

            return total_size

    def calc_chunk(self, total_size: int, chunk: int) -> list:
        # 计算片段大小
        # 片段大小
        piece_size = int(total_size / chunk)
        chunk_list = []

        for i in range(chunk):
            start = i * piece_size + 1 if i != 0 else 0 
            end = (i + 1) * piece_size if i != chunk - 1 else total_size

            chunk_list.append([start, end])

        return chunk_list

    def format_speed(self, speed: int) -> str:
        # 格式化速度信息
        return "{:.1f} MB/s".format(speed / 1024) if speed > 1024 else "{:.1f} KB/s".format(speed) if speed > 0 else ""
