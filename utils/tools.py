import re
import os
import json
import requests

from .config import Config

quality_wrap = {"超高清 8K":127, "杜比视界":126, "真彩 HDR":125, "超清 4K":120, "高清 1080P60":116, "高清 1080P+":112, "高清 1080P":80, "高清 720P":64, "清晰 480P":32, "流畅 360P":16}
codec_wrap = {"AVC": 0, "HEVC": 1, "AV1": 2}

# 获取真实链接
def process_shortlink(url: str):
    if not url.startswith("https"):
        url = "https://" + url

    return requests.get(url, headers = get_header(), proxies = get_proxy()).url

# 获取合法文件名
def get_legal_name(name: str):
    return re.sub('[/\:*?"<>|]', "", name)

# 获取请求头
def get_header(referer_url = None, cookie = None, chunk_list = None) -> dict:
    header = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36"}
    header["Cookie"] = "CURRENT_FNVAL=4048"

    if referer_url != None:
        header["Referer"] = referer_url

    if chunk_list != None:
        header["Range"] = "bytes={}-{}".format(chunk_list[0], chunk_list[1])

    if cookie != None and cookie != "":
        header["Cookie"] += ";SESSDATA=" + cookie
    
    return header

# 获取代理
def get_proxy():
    proxy = {}

    if Config.enable_proxy:
        proxy["http"] = "{}:{}".format(Config.proxy_ip, Config.proxy_port)

    return proxy

# 删除多个文件
def remove_files(path: str, name: list):
    for i in name:
        os.remove(os.path.join(path, i))

# 获取文件大小
def format_size(size: int) -> str:
    if size > 1048576:
        return "{:.1f} GB".format(size / 1024 / 1024)
    elif size > 1024:
        return "{:.1f} MB".format(size / 1024)
    else:
        return "{:.1f} KB".format(size)

# 将 web 文件保存到本地
def save_pic(contents, path: str):
    with open(path, "wb") as f:
        f.write(contents)

# 获取头像
def get_face_pic(url: str):
    face_path = os.path.join(os.getcwd(), "res", "face.jpg")
    
    # 判断图片是否存在，若不存在则下载到本地
    if not os.path.exists(face_path):
        save_pic(requests.get(url).content, face_path)

    return face_path

# 获取等级
def get_level_pic(level: int):
    web_url = "https://scottsloan.github.io/Bili23-Downloader/level/level{}.png".format(level)
    level_path = os.path.join(os.getcwd(), "res", "level.png")
    
    # 判断图片是否存在，若不存在则下载到本地
    if not os.path.exists(level_path):
        save_pic(requests.get(web_url).content, level_path)
    
    return level_path
    
# 检查更新
def check_update():
    update_request = requests.get("https://scottsloan.github.io/Bili23-Downloader/update.json")
    update_json = json.loads(update_request.text)

    return update_json

# 查找字符串
def find_str(pattern: str, string: str):
    if len(re.findall(pattern, string)) != 0: return True
    else: return False

def format_bangumi_title(episode):
    from .bangumi import BangumiInfo

    if BangumiInfo.type == "电影":
        return "{} {}".format(BangumiInfo.title, episode["title"])
    else:
        return episode["share_copy"]
        
# 格式化数据
def format_data(data: int) -> str:
    if data >= 100000000:
        return "{:.1f}亿".format(data / 100000000)
    elif data >= 10000:
        return "{:.1f}万".format(data / 10000)
    else:
        return str(data)

# 获取视频时长
def format_duration(duration: int):
    if duration > 10000:
        duration = duration / 1000

    hours = int(duration // 3600)
    mins = int((duration - hours * 3600) // 60)
    secs = int(duration - hours * 3600 - mins * 60)
    
    return str(hours).zfill(2) + ":" + str(mins).zfill(2) + ":" + str(secs).zfill(2) if hours != 0 else str(mins).zfill(2) + ":" + str(secs).zfill(2)