import re
import requests
import json

from .tools import *
from .config import Config

class VideoInfo:
    # 视频信息

    url = bvid = ""
    
    aid = cid = 0

    title = desc = ""
    
    view = like = coin = danmaku = favorite = reply = ""

    quality = duration = 0

    pages = down_pages = episodes = []

    quality_id = quality_desc = []

    multiple = collection = ""

class ProcessError(Exception):
    pass

class VideoParser:
    def __init__(self, onError, onRedirect):
        self.onError = onError
        self.onRedirect = onRedirect

    @property
    def aid_api(self):
        # 用于通过 aid 获取到 bvid
        return "https://api.bilibili.com/x/web-interface/archive/stat?aid=" + VideoInfo.aid
    
    @property
    def info_api(self):
        # 用于查询视频信息
        return "https://api.bilibili.com/x/web-interface/view?bvid=" + VideoInfo.bvid

    @property
    def quality_api(self):
        # 用于查询视频的清晰度列表
        return "https://api.bilibili.com/x/player/playurl?bvid={}&cid={}&qn=0&fnver=0&fnval=4048&fourk=1".format(VideoInfo.bvid, VideoInfo.cid)
    
    def get_aid(self, url: str):
        # 获取视频 aid
        VideoInfo.aid = re.findall(r"av[0-9]*", url)[0][2:]
        
        aid_request = requests.get(self.aid_api, headers = get_header(), proxies = get_proxy())
        aid_json = json.loads(aid_request.text)

        self.check_json(aid_json)

        bvid = aid_json["data"]["bvid"]
        self.set_bvid(bvid)

    def get_bvid(self, url: str):
        # 获取视频 bvid
        bvid = re.findall(r"BV\w*", url)[0]
        self.set_bvid(bvid)

    def set_bvid(self, bvid: str):
        # 保存视频 bvid 和 url
        VideoInfo.bvid, VideoInfo.url = bvid, "https://www.bilibili.com/video/" + bvid

    def get_video_info(self):
        # 获取视频信息
        info_request = requests.get(self.info_api, headers = get_header(VideoInfo.url, cookie = Config.user_sessdata), proxies = get_proxy())
        info_json = json.loads(info_request.text)

        self.check_json(info_json)

        info_data = info_json["data"]

        # 检测是否为番组链接，如果是，则跳转
        if "redirect_url" in info_data:
            self.onRedirect(info_data["redirect_url"])
            raise ProcessError("Bangumi type detect")
        
        VideoInfo.title = info_data["title"]
        VideoInfo.desc = info_data["desc"] if info_data["desc"] != "-" else "暂无简介"
        VideoInfo.duration = info_data["duration"]
        VideoInfo.cid = info_data["cid"]
        VideoInfo.pages = info_data["pages"]

        # 判断是否为合集视频
        if "ugc_season" in info_data:
            VideoInfo.collection = True

            info_ugc_season = info_data["ugc_season"]
            VideoInfo.title = info_ugc_season["title"]

            VideoInfo.episodes = info_ugc_season["sections"][0]["episodes"]
        else:
            VideoInfo.collection = False
            VideoInfo.episodes = []

            if len(VideoInfo.pages) > 0:
                VideoInfo.multiple = True

        info_stat = info_data["stat"]
        VideoInfo.view = format_data(info_stat["view"])
        VideoInfo.like = format_data(info_stat["like"])
        VideoInfo.coin = format_data(info_stat["coin"])
        VideoInfo.danmaku = format_data(info_stat["danmaku"])
        VideoInfo.favorite = format_data(info_stat["favorite"])
        VideoInfo.reply = format_data(info_stat["reply"])

    def get_video_quality(self):
        # 获取视频清晰度列表
        video_request = requests.get(self.quality_api, headers = get_header(VideoInfo.url, Config.user_sessdata), proxies = get_proxy())
        video_json = json.loads(video_request.text)

        self.check_json(video_json)

        json_data = video_json["data"]

        VideoInfo.quality_id = json_data["accept_quality"]
        VideoInfo.quality_desc = json_data["accept_description"]

    def parse_url(self, url: str):
        # 解析视频链接
        
        if "av" in url:
            self.get_aid(url)
        else:
            self.get_bvid(url)
        
        self.get_video_info()
        self.get_video_quality()
    
    def check_json(self, json):
        # 检查是否请求失败
        if json["code"] != 0:
            self.onError(400)
