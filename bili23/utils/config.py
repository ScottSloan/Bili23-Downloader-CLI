import os
import platform
import subprocess
from configparser import RawConfigParser

class Config:
    config_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "config.conf")
    
    dir = ""
    thread = 4
    codec = "HEVC"
    quality = 80
    sessdata = ""

    download_all = False
    show_quality_list = False
    quiet = False
    edit = False

    danmaku = False
    subtitle = False
    lyric = False
    
    app_name = "Bili23 Downloader CLI"
    app_version = "1.11"
    app_version_code = 111
    app_date = "2022-12-11"
    app_website = "https://github.com/ScottSloan/Bili23-Downloader-CLI"

    platform = platform.platform()

    ffmpeg_available = True if subprocess.call(args = "ffmpeg -version", shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE) == 0 else False

def read_config():
    conf = RawConfigParser()
    conf.read(Config.config_path, encoding = "utf-8")

    Config.dir = conf.get("config", "dir")
    Config.thread = conf.getint("config", "thread")
    Config.quality = conf.getint("config", "quality")
    Config.codec = conf.get("config", "codec")
    Config.sessdata = conf.get("config", "sessdata")

read_config()