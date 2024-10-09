import re
import requests
import json

from .tools import *
from .config import Config
from .api import API

class VideoInfo:
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

    def get_aid(self, url):
        VideoInfo.aid = re.findall(r"av[0-9]*", url)[0][2:]
        
        url = API.Video.aid_url_api(VideoInfo.aid)

        aid_request = requests.get(url, headers = get_header())
        aid_json = json.loads(aid_request.text)

        self.check_json(aid_json)

        bvid = aid_json["data"]["bvid"]
        self.set_bvid(bvid)

    def get_bvid(self, url):
        bvid = re.findall(r"BV\w*", url)[0]
        self.set_bvid(bvid)

    def set_bvid(self, bvid):
        VideoInfo.bvid, VideoInfo.url = bvid, API.URL.bvid_url_api(bvid)

    def get_video_info(self):
        url = API.Video.info_api(VideoInfo.bvid)

        info_request = requests.get(url, headers = get_header(VideoInfo.url, cookie = Config.sessdata))
        info_json = json.loads(info_request.text)

        self.check_json(info_json)

        info_data = info_json["data"]

        if "redirect_url" in info_data:
            self.onRedirect(info_data["redirect_url"])
            raise ProcessError("Bangumi type detect")
        
        VideoInfo.title = info_data["title"]
        VideoInfo.desc = info_data["desc"] if info_data["desc"] != "-" else "暂无简介"
        VideoInfo.duration = info_data["duration"]
        VideoInfo.cid = info_data["cid"]
        VideoInfo.pages = info_data["pages"]

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
        url = API.Video.download_api(VideoInfo.bvid, VideoInfo.cid)

        video_request = requests.get(url, headers = get_header(cookie = Config.sessdata))
        video_json = json.loads(video_request.text)

        self.check_json(video_json)

        json_data = video_json["data"]

        VideoInfo.quality_id = json_data["accept_quality"]
        VideoInfo.quality_desc = json_data["accept_description"]

    def parse_url(self, url: str):
        if "av" in url:
            self.get_aid(url)
        else:
            self.get_bvid(url)
        
        self.get_video_info()
        self.get_video_quality()
    
    def check_json(self, json):
        if json["code"] != 0:
            self.onError(400)
